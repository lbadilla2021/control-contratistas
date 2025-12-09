import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.core.database import get_session
from app.main import app
from app.models.db import Base


test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)


async def override_get_session():
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    app.dependency_overrides[get_session] = override_get_session
    yield
    app.dependency_overrides.pop(get_session, None)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest.fixture(autouse=True)
async def clean_tables():
    yield
    async with test_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as async_client:
        yield async_client


async def test_company_crud(client: AsyncClient):
    create_payload = {
        "name": "Acme Corp",
        "tax_id": "ACM123",
        "compliance_expires_at": "2025-01-01T00:00:00Z",
    }

    create_response = await client.post("/companies/", json=create_payload)
    assert create_response.status_code == 201
    company = create_response.json()
    assert company["name"] == "Acme Corp"

    list_response = await client.get("/companies/")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    detail_response = await client.get(f"/companies/{company['id']}")
    assert detail_response.status_code == 200
    assert detail_response.json()["tax_id"] == "ACM123"

    update_payload = {
        "name": "Acme Updated",
        "tax_id": "ACM123",
        "compliance_expires_at": "2025-02-01T00:00:00Z",
    }
    update_response = await client.put(f"/companies/{company['id']}", json=update_payload)
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Acme Updated"

    delete_response = await client.delete(f"/companies/{company['id']}")
    assert delete_response.status_code == 204

    missing_response = await client.get(f"/companies/{company['id']}")
    assert missing_response.status_code == 404


async def test_worker_crud(client: AsyncClient):
    company_response = await client.post(
        "/companies/",
        json={
            "name": "Builders",
            "tax_id": "BLD456",
            "compliance_expires_at": "2025-03-01T00:00:00Z",
        },
    )
    company_id = company_response.json()["id"]

    worker_payload = {
        "company_id": company_id,
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "certification_expires_at": "2025-04-01T00:00:00Z",
    }

    create_response = await client.post("/workers/", json=worker_payload)
    assert create_response.status_code == 201
    worker = create_response.json()
    assert worker["company_id"] == company_id

    list_response = await client.get("/workers/")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    detail_response = await client.get(f"/workers/{worker['id']}")
    assert detail_response.status_code == 200
    assert detail_response.json()["email"] == "jane.doe@example.com"

    update_payload = {**worker_payload, "last_name": "Smith"}
    update_response = await client.put(f"/workers/{worker['id']}", json=update_payload)
    assert update_response.status_code == 200
    assert update_response.json()["last_name"] == "Smith"

    delete_response = await client.delete(f"/workers/{worker['id']}")
    assert delete_response.status_code == 204

    missing_response = await client.get(f"/workers/{worker['id']}")
    assert missing_response.status_code == 404


async def test_worker_requires_company(client: AsyncClient):
    worker_payload = {
        "company_id": 999,
        "first_name": "Ghost",
        "last_name": "User",
        "email": "ghost@example.com",
        "certification_expires_at": "2025-05-01T00:00:00Z",
    }

    response = await client.post("/workers/", json=worker_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Company not found"

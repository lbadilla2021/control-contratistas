import pytest


@pytest.mark.asyncio
async def test_create_worker_for_company(client):
    company_payload = {"name": "Gamma Inc", "tax_id": "GAM-001"}
    company_resp = await client.post("/companies/", json=company_payload)
    company_id = company_resp.json()["id"]

    worker_payload = {
        "company_id": company_id,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
    }
    worker_resp = await client.post("/workers/", json=worker_payload)
    assert worker_resp.status_code == 201
    worker_body = worker_resp.json()
    assert worker_body["company_id"] == company_id
    assert worker_body["first_name"] == "John"

    get_resp = await client.get(f"/workers/{worker_body['id']}")
    assert get_resp.status_code == 200
    assert get_resp.json()["email"] == "john.doe@example.com"


@pytest.mark.asyncio
async def test_update_and_delete_worker(client):
    company_resp = await client.post(
        "/companies/", json={"name": "Delta", "tax_id": "DEL-55"}
    )
    company_id = company_resp.json()["id"]

    worker_resp = await client.post(
        "/workers/",
        json={
            "company_id": company_id,
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com",
        },
    )
    worker_id = worker_resp.json()["id"]

    update_resp = await client.put(
        f"/workers/{worker_id}",
        json={
            "company_id": company_id,
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
        },
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["email"] == "jane.smith@example.com"

    delete_resp = await client.delete(f"/workers/{worker_id}")
    assert delete_resp.status_code == 204

    missing_resp = await client.get(f"/workers/{worker_id}")
    assert missing_resp.status_code == 404

import pytest


@pytest.mark.asyncio
async def test_create_and_get_company(client):
    create_payload = {"name": "Acme Corp", "tax_id": "ACME-123"}
    response = await client.post("/companies/", json=create_payload)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == create_payload["name"]
    assert body["tax_id"] == create_payload["tax_id"]

    company_id = body["id"]
    get_response = await client.get(f"/companies/{company_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == company_id


@pytest.mark.asyncio
async def test_update_and_delete_company(client):
    create_payload = {"name": "Beta LLC", "tax_id": "BETA-999"}
    response = await client.post("/companies/", json=create_payload)
    company_id = response.json()["id"]

    update_payload = {"name": "Beta Updated", "tax_id": "BETA-999"}
    update_response = await client.put(
        f"/companies/{company_id}", json=update_payload
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Beta Updated"

    delete_response = await client.delete(f"/companies/{company_id}")
    assert delete_response.status_code == 204

    missing_response = await client.get(f"/companies/{company_id}")
    assert missing_response.status_code == 404

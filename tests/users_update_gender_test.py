import pytest

from httpx import AsyncClient


@pytest.mark.asyncio
async def test_update_gender(client: AsyncClient):
    login_response = await client.post(
        "/users/loginByInitData",
        data={"init_data": "test"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["user"]["token"]["accessToken"]

    response = await client.put(
        "/users/updateGender",
        json={"gender": "male"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["gender"] == "male"

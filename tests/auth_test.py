import pytest

from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_by_init_data(client: AsyncClient):
    init_data = "test"

    response = await client.post(
        "/users/loginByInitData",
        data={"init_data": init_data},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert "user" in data
    assert "accessToken" in data["user"]["token"]
    assert "refreshToken" in data["user"]["token"]
    assert isinstance(data["user"]["id"], int)
    assert data["user"]["tokensCount"] == 0

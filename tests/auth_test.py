import pytest

from httpx import AsyncClient

from photogen_api.auth.jwt import create_refresh_token
from photogen_api.database.models.user import User


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


@pytest.mark.asyncio
async def test_refresh_token_success(client: AsyncClient):
    user = await User.create(telegram_id="999999", role="user")
    refresh = create_refresh_token({"sub": str(user.id)})

    response = await client.post("/users/refresh", json={"refreshToken": refresh})

    assert response.status_code == 200
    data = response.json()
    assert "accessToken" in data
    assert "refreshToken" in data


@pytest.mark.asyncio
async def test_refresh_token_invalid(client: AsyncClient):
    response = await client.post("/users/refresh", json={"refreshToken": "invalid.token.here"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"
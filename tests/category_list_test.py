import pytest

from httpx import AsyncClient

from photogen_api.auth.jwt import create_access_token
from photogen_api.database.models.user import User


@pytest.mark.asyncio
async def test_get_categories(client: AsyncClient):
    user = await User.create(telegram_id="123", role="user")

    from photogen_api.database.models.category import Category
    await Category.create(title="Deep-Dark-Fantasy", preview="url1")
    await Category.create(title="Sci-Fi", preview="url2")

    token = create_access_token({"sub": str(user.id)})

    response = await client.get(
        "/categories/?page=1&limit=10",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["categories"]) == 2

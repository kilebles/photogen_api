import pytest

from httpx import AsyncClient

from photogen_api.auth.jwt import create_access_token
from photogen_api.database.models.user import User
from photogen_api.database.models.style import Style
from photogen_api.database.models.category import Category  


@pytest.mark.asyncio
async def test_get_styles(client: AsyncClient):
    user = await User.create(telegram_id="123", role="user")

    await Style.create(title="Anime", prompt="anime style", position=1)
    await Style.create(title="Realistic", prompt="realistic style", position=2)

    token = create_access_token({"sub": str(user.id)})

    response = await client.get(
        "/styles/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["styles"]) == 2
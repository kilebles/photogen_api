import pytest

from httpx import AsyncClient
from photogen_api.auth.jwt import create_access_token
from photogen_api.database.models.user import User
from photogen_api.database.models.user_profile import UserProfile

@pytest.mark.asyncio
async def test_get_profiles_with_metadata(client: AsyncClient):
    user = await User.create(telegram_id="123", role="user")
    await UserProfile.create(
        user=user,
        lora_id="lora_123",
        status="ready",
        job_id=101,
        photos=["/media/profiles/sample1.jpg", "/media/profiles/sample2.jpg"],
    )

    token = create_access_token({"sub": str(user.id)})

    response = await client.get(
        "/users/profiles/meta",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["profiles"], list)
    assert data["profiles"][0]["loraId"] == "lora_123"
    assert data["profiles"][0]["status"] == "ready"
    assert data["profiles"][0]["jobId"] == 101
    assert isinstance(data["profiles"][0]["photos"], list)
    assert "/media/profiles/sample1.jpg" in data["profiles"][0]["photos"]

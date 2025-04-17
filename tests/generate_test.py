import pytest

from httpx import AsyncClient

from photogen_api.auth.jwt import create_access_token
from photogen_api.database.models.category import Category
from photogen_api.database.models.generation import Generation
from photogen_api.database.models.user import User
from photogen_api.database.models.user_job import UserJob


@pytest.mark.asyncio
async def test_generate_with_prompt(client: AsyncClient):
    user = await User.create(telegram_id="123", role="user")
    token = create_access_token({"sub": str(user.id)})

    response = await client.post(
        "/generations/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "profileId": 1,
            "prompt": "A futuristic city",
            "resolution": "1024x1024"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["jobId"], int)


@pytest.mark.asyncio
async def test_get_generation_status(client: AsyncClient):
    user = await User.create(telegram_id="123", role="user")
    category = await Category.create(title="TestCategory", preview="some_url")
    job = await UserJob.create(user=user, job_id="gen123", job_type="generation", status="completed")

    await Generation.create(
        user=user,
        job=job,
        category=category,
        image_url="https://example.com/image1.png",
        prompt="test prompt",
        resolution="512x512",
        status="completed"
    )
    await Generation.create(
        user=user,
        job=job,
        category=category,
        image_url="https://example.com/image2.png",
        prompt="test prompt",
        resolution="512x512",
        status="completed"
    )

    token = create_access_token({"sub": str(user.id)})

    response = await client.get(
        f"/generations/{job.id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["status"] == "completed"
    assert isinstance(data["result"], list)
    assert len(data["result"]) == 2
    assert "https://example.com/image1.png" in data["result"]
    assert "https://example.com/image2.png" in data["result"]
    
    
@pytest.mark.asyncio
async def test_list_user_generations(client: AsyncClient):
    user = await User.create(telegram_id="123", role="user")
    category = await Category.create(title="Fantasy", preview="some_url")

    await Generation.create(
        user=user,
        category=category,
        image_url="https://example.com/image1.png",
        prompt="dragon",
        resolution="512x512",
        status="completed"
    )
    await Generation.create(
        user=user,
        category=category,
        image_url="https://example.com/image2.png",
        prompt="castle",
        resolution="512x512",
        status="completed"
    )

    token = create_access_token({"sub": str(user.id)})

    response = await client.get(
        "/users/generations?page=1&limit=10",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["generations"]) == 2
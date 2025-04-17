import pytest

from httpx import AsyncClient


@pytest.mark.asyncio
async def test_upload_profile(client: AsyncClient):
    login_response = await client.post(
        "/users/loginByInitData",
        data={"init_data": "test"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["user"]["token"]["accessToken"]

    files = [
        ("images", ("image1.png", b"fake image data 1", "image/png")),
        ("images", ("image2.jpg", b"fake image data 2", "image/jpeg")),
    ]

    response = await client.post(
        "/users/uploadProfile",
        files=files,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["images"], list)
    assert len(data["images"]) == 2

import re
import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_upload_profile(client: AsyncClient):
    fake_job_id = "fake-job-id-123"
    mock_fn = AsyncMock(return_value=fake_job_id)

    with patch(
        "photogen_api.routes.users_router.start_replicate_generation",
        new=mock_fn,
    ):
        login_resp = await client.post(
            "/users/loginByInitData",
            data={"init_data": "test"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert login_resp.status_code == 200
        token = login_resp.json()["user"]["token"]["accessToken"]

        files = [
            ("images", ("image1.png", b"fake data 1", "image/png")),
            ("images", ("image2.jpg", b"fake data 2", "image/jpeg")),
        ]

        resp = await client.post(
            "/users/uploadProfile",
            files=files,
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert len(body["images"]) == len(files)

    for returned, sent in zip(body["images"], files):
        original_name = sent[1][0]
        assert returned.startswith("/media/profiles/")
        assert returned.endswith(original_name)
        assert re.search(r"/media/profiles/[0-9a-f]{32}_"+re.escape(original_name)+r"$", returned)

    user_id = str(login_resp.json()["user"]["id"])
    mock_fn.assert_awaited_once_with(prompt="train profile", webhook_id=user_id)

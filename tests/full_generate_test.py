import json
import time
import hmac
import base64
import hashlib
from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient

from photogen_api.auth.jwt import create_access_token
from photogen_api.config import config
from photogen_api.database.models.user import User
from photogen_api.database.models.user_job import UserJob
from photogen_api.database.models.generation import Generation


@pytest.mark.asyncio
async def test_full_generation_flow(client: AsyncClient, monkeypatch):
    pred_id = "pred_123"

    monkeypatch.setattr(
        "photogen_api.services.generation_service.start_replicate_generation",
        AsyncMock(return_value=pred_id),
    )

    user = await User.create(telegram_id="42", role="user")
    token = create_access_token({"sub": str(user.id)})

    resp = await client.post(
        "/generations/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "prompt": "Hello world",
            "profileId": 1,
            "resolution": "512x512",
        },
    )
    assert resp.status_code == 200
    job_pk: int = resp.json()["jobId"]

    job = await UserJob.get(id=job_pk)
    assert job.job_id == pred_id
    assert job.status == "waiting"

    webhook_id = str(user.id)
    ts = str(int(time.time()))
    payload = {"id": pred_id, "status": "succeeded",
               "output": ["img1.png", "img2.png"]}
    body = json.dumps(payload)

    secret = base64.b64decode(config.REPLICATE_WEBHOOK_SECRET.split("_", 1)[1])
    msg = f"{webhook_id}.{ts}.{body}".encode()
    signature = base64.b64encode(hmac.new(secret, msg, hashlib.sha256).digest()).decode()

    headers = {
        "webhook-id": webhook_id,
        "webhook-timestamp": ts,
        "webhook-signature": f"v1,{signature}",
        "Content-Type": "application/json",
    }
    hook_resp = await client.post("/replicate/webhook", headers=headers, content=body)
    assert hook_resp.status_code == 200
    assert hook_resp.json() == {"success": True}

    job = await UserJob.get(id=job_pk)
    assert job.status == "succeeded"

    gens = await Generation.filter(job_id=job_pk).order_by("id")
    assert len(gens) == 2
    assert [g.image_url for g in gens] == ["img1.png", "img2.png"]

import time
import json
import hmac
import base64
import hashlib
import pytest

from photogen_api.config import config


@pytest.mark.asyncio
async def test_replicate_webhook_success(client):
    payload = {
        "id": "pred_123",
        "status": "succeeded",
        "output": ["https://cdn.replicate.com/output1.png"],
    }
    body = json.dumps(payload)

    webhook_id = "test-webhook-id"
    timestamp = str(int(time.time()))

    secret_b64 = config.REPLICATE_WEBHOOK_SECRET.split("_", 1)[1]
    secret_key = base64.b64decode(secret_b64)

    signed = f"{webhook_id}.{timestamp}.{body}".encode()
    digest = hmac.new(secret_key, signed, hashlib.sha256).digest()
    signature = base64.b64encode(digest).decode()
    signature_header = f"v1,{signature}"

    headers = {
        "webhook-id": webhook_id,
        "webhook-timestamp": timestamp,
        "webhook-signature": signature_header,
        "Content-Type": "application/json",
    }

    resp = await client.post("/replicate/webhook", content=body, headers=headers)

    assert resp.status_code == 200
    assert resp.json() == {"success": True}


@pytest.mark.asyncio
async def test_replicate_webhook_bad_signature(client):
    body = json.dumps({"id": "pred_123", "status": "succeeded"})

    resp = await client.post("/replicate/webhook", content=body)
    assert resp.status_code == 403
    assert resp.json()["detail"] == "Invalid signature"

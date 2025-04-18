import json
import hmac
import base64
import hashlib
import logging

from fastapi import APIRouter, Request, HTTPException, status
from photogen_api.config import config
from photogen_api.database.models.user_job import UserJob
from photogen_api.database.models.generation import Generation

router = APIRouter(tags=["Replicate"], prefix="/replicate")
logger = logging.getLogger(__name__)


def verify_replicate_signature(request: Request, body: bytes) -> bool:
    header_signature = request.headers.get("webhook-signature")
    header_id = request.headers.get("webhook-id")
    header_ts = request.headers.get("webhook-timestamp")
    if not (header_signature and header_id and header_ts):
        return False

    message = f"{header_id}.{header_ts}.{body.decode()}".encode()
    secret_b64 = config.REPLICATE_WEBHOOK_SECRET.split("_", 1)[1]
    secret = base64.b64decode(secret_b64)
    digest = hmac.new(secret, message, hashlib.sha256).digest()
    computed_sig = base64.b64encode(digest).decode()

    try:
        _version, sent_sig = header_signature.split(",", 1)
    except ValueError:
        return False

    return hmac.compare_digest(computed_sig, sent_sig)


@router.post("/webhook")
async def replicate_webhook(request: Request):
    body = await request.body()
    if not verify_replicate_signature(request, body):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid signature")

    data = json.loads(body)
    pred_id = data.get("id")
    status_ = data.get("status")
    output = data.get("output") or []

    job = await UserJob.filter(job_id=pred_id).first()
    if not job:
        return {"success": True}

    job.status = status_
    await job.save()

    urls = output if isinstance(output, list) else [output]
    for url in urls:
        await Generation.create(
            user_id=job.user_id,
            job=job,
            category_id=None,
            style_id=None,
            image_url=url,
            prompt="",
            resolution=None,
            status=status_,
        )

    logger.info(f"[Replicate] job {job.id} → {status_}, {len(urls)} images")
    return {"success": True}

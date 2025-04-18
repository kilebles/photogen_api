import httpx

from fastapi import HTTPException
from photogen_api.config import config


async def start_replicate_generation(prompt: str, webhook_id: str) -> str:
    headers = {
        "Authorization": f"Token {config.REPLICATE_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        """либо только version, либо slug+version"""
    
        # "model": config.REPLICATE_MODEL_SLUG,
        "version": config.REPLICATE_MODEL_VERSION,
        "input": {"prompt": prompt},
        "webhook": f"{config.APP_URL}replicate/webhook",
        "webhook_events_filter": ["completed"],
        "webhook_id": webhook_id,
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(config.REPLICATE_API_URL, json=payload, headers=headers)

    if resp.status_code != 201:
        raise HTTPException(status_code=500, detail="Failed to start generation on Replicate")

    data = resp.json()
    return data["id"]

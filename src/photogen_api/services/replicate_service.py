import logging
import time
import zipfile
import anyio
import httpx
import replicate

from uuid import uuid4
from pathlib import Path
from fastapi import HTTPException

from photogen_api.config import config


async def start_replicate_generation(prompt: str, webhook_id: str) -> str:
    headers = {
        "Authorization": f"Token {config.REPLICATE_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "version": config.REPLICATE_MODEL_VERSION,
        "input": {
            "prompt": prompt,
            "webhook_id": webhook_id
        },
        "webhook": f"{config.APP_URL}replicate/webhook",
        "webhook_events_filter": ["completed"],
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(config.REPLICATE_API_URL, json=payload, headers=headers)

    if resp.status_code != 201:
        logging.error(f"Replicate API error {resp.status_code}: {resp.text}")
        raise HTTPException(status_code=500, detail="Failed to start generation on Replicate")

    data = resp.json()
    return data["id"]


async def start_replicate_training(user_id: int, image_paths: list[str]) -> str:
    """
    1) Собирает ZIP из локальных файлов image_paths
    2) Сохраняет его в папку media/profiles
    3) Стартует тренировку на Replicate в заранее созданном репозитории
    4) Возвращает training_id
    """

    zip_name = f"{uuid4().hex}.zip"
    media_dir = Path("media/profiles")
    media_dir.mkdir(parents=True, exist_ok=True)
    zip_path = media_dir / zip_name

    with zipfile.ZipFile(zip_path, "w") as archive:
        for rel in image_paths:
            src = Path(rel.lstrip("/"))
            archive.write(src, arcname=src.name)

    archive_url = f"{config.APP_URL.rstrip('/')}/media/profiles/{zip_name}"

    def _sync_train() -> str:
        client = replicate.Client(api_token=config.REPLICATE_TOKEN)

        destination = config.REPLICATE_TRAIN_MODEL_SLUG  
        version = config.REPLICATE_TRAIN_VERSION

        training = client.trainings.create(
            destination=destination,
            version=version,
            input={
                "input_images": archive_url,
                "steps": 1000,
                "lora_rank": 16,
                "optimizer": "adamw8bit",
                "batch_size": 1,
                "resolution": "512,768,1024",
                "autocaption": True,
                "trigger_word": "TOK",
                "learning_rate": 0.0004,
                "wandb_project": "flux_train_replicate",
                "wandb_save_interval": 100,
                "caption_dropout_rate": 0.05,
                "cache_latents_to_disk": False,
                "wandb_sample_interval": 100,
                "gradient_checkpointing": False,
            },
            webhook=f"{config.APP_URL.rstrip('/')}/replicate/webhook",
            webhook_events_filter=["completed"],
        )

        return training.id

    train_id = await anyio.to_thread.run_sync(_sync_train)
    if not train_id:
        raise HTTPException(status_code=500, detail="Failed to start Replicate training")

    return train_id
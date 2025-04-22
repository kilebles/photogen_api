from uuid import uuid4
from pathlib import Path

from fastapi import APIRouter, Depends, File, Query, UploadFile
from typing import List

from photogen_api.auth.dep import get_current_user
from photogen_api.database.models.user import User
from photogen_api.database.models.user_job import UserJob
from photogen_api.database.models.user_profile import UserProfile
from photogen_api.schemas.generation import GetGenerationsResponse, UploadImagesResponse
from photogen_api.schemas.profile import GetProfilesWithMetaResponse
from photogen_api.schemas.user import UpdateGenderRequest, UpdateGenderResponse
from photogen_api.services.generation_service import get_user_generations
from photogen_api.services.replicate_service import start_replicate_training
from photogen_api.config import config
from photogen_api.services.user_service import get_profiles_with_metadata, update_user_gender

router = APIRouter(prefix="/users", tags=["Users"])


@router.put("/updateGender", response_model=UpdateGenderResponse)
async def update_gender(
    body: UpdateGenderRequest,
    user: User = Depends(get_current_user)
):
    return await update_user_gender(user, body.gender)


@router.post("/uploadProfile", response_model=UploadImagesResponse)
async def upload_profile_images(
    images: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
):
    rel_paths: list[str] = []
    for img in images:
        filename = f"{uuid4().hex}_{img.filename}"
        rel = f"/media/profiles/{filename}"
        dst = Path(rel.lstrip("/"))
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(await img.read())
        rel_paths.append(rel)

    external_job_id = await start_replicate_training(
        user_id=current_user.id,
        image_paths=rel_paths,
    )

    job = await UserJob.create(
        user=current_user,
        job_id=external_job_id,
        job_type="training",
        status="pending",
    )
    profile, _ = await UserProfile.get_or_create(user=current_user)
    profile.job_id = job.id
    profile.status = "pending"
    profile.photos = rel_paths
    await profile.save()

    return UploadImagesResponse(success=True, images=rel_paths)


@router.get("/generations", response_model=GetGenerationsResponse)
async def list_user_generations(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    user: User = Depends(get_current_user),
):
    return await get_user_generations(user.id, page, limit)


@router.get("/profiles/meta", response_model=GetProfilesWithMetaResponse)
async def list_profiles_with_metadata(
    user: User = Depends(get_current_user)
):
    return await get_profiles_with_metadata(user.id)
import os

from typing import List
from uuid import uuid4
from fastapi import APIRouter, Depends, File, Query, UploadFile

from photogen_api.auth.dep import get_current_user
from photogen_api.database.models.user import User
from photogen_api.schemas.generation import GetGenerationsResponse, UploadImagesResponse
from photogen_api.schemas.profile import GetProfilesResponse, GetProfilesWithMetaResponse
from photogen_api.schemas.user import UpdateGenderRequest, UpdateGenderResponse
from photogen_api.services.generation_service import get_user_generations
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
    current_user: User = Depends(get_current_user)
):
    saved_paths = []

    for image in images:
        filename = f"{uuid4().hex}_{image.filename}"
        path = f"media/profiles/{filename}"
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "wb") as f:
            f.write(await image.read())

        saved_paths.append(f"/{path}")

    # TODO: Save paths to the database

    return UploadImagesResponse(success=True, images=saved_paths)


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
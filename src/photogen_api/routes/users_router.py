import os

from typing import List
from uuid import uuid4
from fastapi import APIRouter, Depends, File, UploadFile

from photogen_api.auth.dep import get_current_user
from photogen_api.database.models.user import User
from photogen_api.schemas.generation import UploadImagesResponse
from photogen_api.schemas.user import UpdateGenderRequest, UpdateGenderResponse
from photogen_api.services.user_service import update_user_gender

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
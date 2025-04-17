from fastapi import APIRouter, Depends

from photogen_api.auth.dep import get_current_user
from photogen_api.schemas.generation import CheckGenerateJobResponse, GenerateRequest, GenerateResponse
from photogen_api.database.models.user import User
from photogen_api.services.generation_service import check_generate_status, generate_image

router = APIRouter(prefix="/generations", tags=["Generations"])


@router.post("/", response_model=GenerateResponse)
async def create_generation(
    request: GenerateRequest,
    user: User = Depends(get_current_user)
):
    return await generate_image(request, user)


@router.get("/{job_id}", response_model=CheckGenerateJobResponse)
async def get_generation_status(
    job_id: int,
    user=Depends(get_current_user)
):
    return await check_generate_status(job_id, user.id)
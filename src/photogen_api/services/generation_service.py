from fastapi import HTTPException, status

from photogen_api.database.models.generation import Generation
from photogen_api.database.models.user_job import UserJob
from photogen_api.schemas.common import JobStatus
from photogen_api.schemas.generation import CheckGenerateJobResponse, GenerateRequest, GenerateResponse, GetGenerationsResponse
from photogen_api.database.models.user import User


async def generate_image(request: GenerateRequest, user: User) -> GenerateResponse:
    if request.prompt and (request.category_id or request.style_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Укажите либо prompt, либо categoryId и styleId"
        )

    if not request.prompt and not (request.category_id and request.style_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Обязателен либо prompt, либо categoryId + styleId"
        )

    user_job = await UserJob.create(
        user=user,
        job_id="mock_job_id",
        job_type="generation",
        status="in_progress"
    )

    generation = await Generation.create(
        user=user,
        job=user_job,
        category_id=request.category_id,
        style_id=request.style_id,
        prompt=request.prompt or "",
        image_url="",
        status="in_progress"
    )

    return GenerateResponse(success=True, job_id=user_job.id)


async def check_generate_status(job_id: int, user_id: int) -> CheckGenerateJobResponse:
    job = await UserJob.filter(id=job_id, user_id=user_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    generations = await Generation.filter(job_id=job_id).all()
    image_urls = [gen.image_url for gen in generations]

    return CheckGenerateJobResponse(
        success=True,
        status=JobStatus(job.status),
        result=image_urls if image_urls else None
    )
    
async def get_user_generations(user_id: int, page: int, limit: int) -> GetGenerationsResponse:
    total = await Generation.filter(user_id=user_id).count()
    generations = (
        await Generation
        .filter(user_id=user_id)
        .offset((page - 1) * limit)
        .limit(limit)
        .order_by("-created_at")
    )

    image_urls = [g.image_url for g in generations]

    return GetGenerationsResponse(
        success=True,
        page=page,
        total_pages=(total + limit - 1) // limit,
        generations=image_urls
    )
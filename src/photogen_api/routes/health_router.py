from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["Health"])
async def health():
    return {"message": "API is running"}
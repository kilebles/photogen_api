from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["Users"])
async def health():
    return {"message": "Users router is running"}
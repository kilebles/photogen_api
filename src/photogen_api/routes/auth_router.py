from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["Auth"])
async def health():
    return {"message": "Auth router is running"}
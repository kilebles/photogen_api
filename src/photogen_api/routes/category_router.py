from fastapi import APIRouter, Depends, Query

from photogen_api.auth.dep import get_current_user
from photogen_api.schemas.category import CategoriesResponse
from photogen_api.services.category_service import get_categories

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=CategoriesResponse)
async def list_categories(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    q: str = Query(""),
    user=Depends(get_current_user)
):
    return await get_categories(page=page, limit=limit, q=q)
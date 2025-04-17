from fastapi import APIRouter, Depends

from photogen_api.auth.dep import get_current_user
from photogen_api.schemas.user import User
from photogen_api.schemas.style import StylesResponse
from photogen_api.services.style_service import get_styles

router = APIRouter(prefix="/styles", tags=["Styles"])


@router.get("/", response_model=StylesResponse)
async def list_styles(_: User = Depends(get_current_user)):
    return await get_styles()

from fastapi import APIRouter, Form
from photogen_api.schemas.auth import LoginResponse, RefreshTokenRequest, RefreshTokenResponse
from photogen_api.services.auth_service import login_by_init_data, refresh_tokens


router = APIRouter(prefix="/users", tags=["Auth"])


@router.post("/loginByInitData", response_model=LoginResponse)
async def login_by_telegram(init_data: str = Form(...)):
    return await login_by_init_data(init_data)


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    return await refresh_tokens(request.refresh_token)
from fastapi import APIRouter, Form
from photogen_api.schemas.auth import LoginResponse
from photogen_api.services.auth_service import login_by_init_data


router = APIRouter(prefix="/users", tags=["Auth"])


@router.post("/loginByInitData", response_model=LoginResponse)
async def login_by_telegram(init_data: str = Form(...)):
    return await login_by_init_data(init_data)
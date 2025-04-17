import json
from fastapi import HTTPException, status
from aiogram.utils import web_app

from photogen_api.config import config
from photogen_api.database.models.user import User
from photogen_api.database.models.user_profile import UserProfile
from photogen_api.auth.jwt import create_access_token, create_refresh_token, validate_refresh_token
from photogen_api.schemas.auth import LoginResponse, RefreshTokenResponse, Token
from photogen_api.schemas.user import User as UserSchema


async def login_by_init_data(init_data: str) -> LoginResponse:
    if init_data == "test": # For testing purposes
        class FakeTelegramUser:
            id = 123456
            first_name = "Test"
            last_name = "User"
            username = "testuser"
            photo_url = None

        tg_user = FakeTelegramUser()
    else:
        try:
            parsed_data = web_app.parse_webapp_init_data(init_data, loads=json.loads)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid init data")

        if not web_app.check_webapp_signature(config.TG_BOT_TOKEN, init_data):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid init data signature")

        tg_user = parsed_data.user

    user = await User.filter(telegram_id=tg_user.id).select_related("profile").first()

    if not user:
        user = await User.create(
            telegram_id=tg_user.id,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            username=tg_user.username,
            photo=tg_user.photo_url,
        )
        await UserProfile.create(user=user)
        await user.fetch_related("profile")

    payload = {"sub": str(user.id)}
    access = create_access_token(payload)
    refresh = create_refresh_token(payload)

    user_schema = UserSchema(
        id=user.id,
        role=user.role,
        photo=user.photo,
        mention=f"@{user.username}" if user.username else user.first_name,
        tokens_count=user.tokens,
        token=Token(access_token=access, refresh_token=refresh),
    )

    return LoginResponse(success=True, user=user_schema)


async def refresh_tokens(refresh_token: str) -> RefreshTokenResponse:
    user = await validate_refresh_token(refresh_token)

    payload = {"sub": str(user.id)}
    new_access = create_access_token(payload)
    new_refresh = create_refresh_token(payload)

    return RefreshTokenResponse(
        access_token=new_access,
        refresh_token=new_refresh,
    )
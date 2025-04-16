from typing import Optional
from pydantic import BaseModel, ConfigDict

from photogen_api.utils import to_camel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    
    model_config = ConfigDict(
        alias_gnerator=to_camel,
        populate_by_name=True
    )

class LoginResponse(BaseModel):
    success: bool
    user: "User"

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


class RefreshTokenRequest(BaseModel):
    refresh_token: str

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


class RefreshTokenResponse(BaseModel):
    access: str
    refresh: str

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


# Forward ref для LoginResponse
from .user import User
LoginResponse.model_rebuild()
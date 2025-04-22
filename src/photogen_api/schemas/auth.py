from typing import TYPE_CHECKING
from pydantic import BaseModel, ConfigDict

from photogen_api.utils import to_camel

if TYPE_CHECKING:
    from photogen_api.schemas.user import User


class Token(BaseModel):
    access_token: str
    refresh_token: str

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class LoginResponse(BaseModel):
    success: bool
    user: "User"

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class RefreshTokenRequest(BaseModel):
    refresh_token: str

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class RefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


from .user import User
LoginResponse.model_rebuild()

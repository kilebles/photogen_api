from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict

from photogen_api.schemas.common import Gender, StatusResponse
from photogen_api.utils import to_camel


class UserRole(str, Enum):
    NEW = "new"
    USER = "user"
    ADMIN = "admin"


class User(BaseModel):
    id: int
    role: UserRole
    photo: Optional[str] = None
    mention: str
    tokens_count: int
    token: Optional["Token"] = None

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class UpdateGenderRequest(BaseModel):
    gender: Gender

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class UpdateGenderResponse(StatusResponse):
    gender: Gender

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


from .auth import Token
User.model_rebuild()

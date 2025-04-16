from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Optional

from photogen_api.utils import to_camel
from photogen_api.schemas.common import Gender, StatusResponse


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
        populate_by_name=True
    )
    

class UpdateGenderRequest(BaseModel):
    gender: Gender

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


class UpdateGenderResponse(StatusResponse):
    gender: Gender

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


# Forward ref для Token
from .auth import Token
User.model_rebuild()

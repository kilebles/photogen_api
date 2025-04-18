from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict

from photogen_api.utils import to_camel


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class JobStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    
    ERROR = "error"


class UserRole(str, Enum):
    NEW = "new"
    USER = "user"
    ADMIN = "admin"


class StatusResponse(BaseModel):
    success: bool
    message: Optional[str] = None

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


class PageResponse(StatusResponse):
    page: int
    total_pages: int

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

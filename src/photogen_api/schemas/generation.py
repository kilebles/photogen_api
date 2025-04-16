from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from photogen_api.schemas.common import JobStatus, StatusResponse, PageResponse
from photogen_api.utils import to_camel


class GenerateRequest(BaseModel):
    profile_id: int
    category_id: Optional[int] = None
    style_id: Optional[int] = None
    prompt: Optional[str] = None
    resolution: str

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


class GenerateResponse(StatusResponse):
    job_id: int

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


class CheckGenerateJobResponse(StatusResponse):
    status: JobStatus
    result: Optional[List[str]] = None

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


class GetGenerationsResponse(PageResponse):
    generations: List[str]

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


class UploadImagesResponse(StatusResponse):
    images: List[str]

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )
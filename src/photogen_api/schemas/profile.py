from typing import List
from pydantic import BaseModel, ConfigDict

from photogen_api.utils import to_camel
from photogen_api.schemas.common import StatusResponse


class ProfilePhotos(BaseModel):
    id: int
    photos: List[str]

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


class GetProfilesResponse(StatusResponse):
    profiles: List[ProfilePhotos]

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


class ProfileWithMetadata(BaseModel):
    id: int
    lora_id: str | None = None
    status: str | None = None
    job_id: int | None = None
    photos: List[str] = []

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


class GetProfilesWithMetaResponse(StatusResponse):
    profiles: List[ProfileWithMetadata]

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )
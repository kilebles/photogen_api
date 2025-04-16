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

from typing import List
from pydantic import BaseModel, ConfigDict

from photogen_api.utils import to_camel


class Style(BaseModel):
    id: int
    title: str

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


class StylesResponse(BaseModel):
    success: bool = True
    styles: List[Style]

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )
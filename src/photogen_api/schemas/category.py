from typing import List
from pydantic import BaseModel, ConfigDict

from photogen_api.utils import to_camel


class Category(BaseModel):
    id: int
    title: str
    preview: str

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


class CategoriesResponse(BaseModel):
    success: bool = True
    categories: List[Category]

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )
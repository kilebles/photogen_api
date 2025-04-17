from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from photogen_api.utils import to_camel


class Category(BaseModel):
    id: int
    title: str
    preview: Optional[str] = None
    gender: Optional[str] = None
    prompt: Optional[str] = None
    position: Optional[int] = None

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
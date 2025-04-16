from photogen_api.database.models.category import Category
from photogen_api.schemas.category import Category as CategorySchema
from photogen_api.schemas.common import PageResponse
from photogen_api.schemas.category import CategoriesResponse


async def get_categories(page: int = 1, limit: int = 10, q: str = "") -> CategoriesResponse:
    query = Category.all()

    if q:
        query = query.filter(title__icontains=q)

    total = await query.count()
    total_pages = (total + limit - 1) // limit
    categories = await query.offset((page - 1) * limit).limit(limit)

    return CategoriesResponse(
        success=True,
        categories=[CategorySchema.model_validate(c, from_attributes=True) for c in categories],
        page=page,
        total_pages=total_pages
    )

from photogen_api.database.models.style import Style
from photogen_api.schemas.style import StylesResponse, Style as StyleSchema


async def get_styles() -> StylesResponse:
    styles = await Style.all().order_by("id")
    return StylesResponse(
        styles=[StyleSchema.model_validate(s, from_attributes=True) for s in styles]
    )

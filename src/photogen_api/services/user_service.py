from fastapi import HTTPException

from photogen_api.database.models.user import User
from photogen_api.schemas.common import Gender
from photogen_api.schemas.user import UpdateGenderResponse


async def update_user_gender(user: User, gender: Gender) -> UpdateGenderResponse:
    user.gender = gender
    await user.save(update_fields=["gender"])
    return UpdateGenderResponse(success=True, gender=gender)
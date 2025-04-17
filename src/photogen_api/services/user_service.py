
from photogen_api.database.models.user import User
from photogen_api.database.models.user_profile import UserProfile
from photogen_api.schemas.common import Gender
from photogen_api.schemas.profile import GetProfilesWithMetaResponse, ProfileWithMetadata
from photogen_api.schemas.user import UpdateGenderResponse


async def update_user_gender(user: User, gender: Gender) -> UpdateGenderResponse:
    user.gender = gender
    await user.save(update_fields=["gender"])
    return UpdateGenderResponse(success=True, gender=gender)


async def get_profiles_with_metadata(user_id: int) -> GetProfilesWithMetaResponse:
    profiles = await UserProfile.filter(user_id=user_id).all()
    return GetProfilesWithMetaResponse(
        success=True,
        profiles=[
            ProfileWithMetadata.model_validate(p, from_attributes=True)
            for p in profiles
        ]
    )
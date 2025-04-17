from fastapi import APIRouter

from photogen_api.routes.health_router import router as health_router
from photogen_api.routes.users_router import router as users_router
from photogen_api.routes.auth_router import router as auth_router
from photogen_api.routes.category_router import router as category_router
from photogen_api.routes.style_router import router as style_router

router = APIRouter()
router.include_router(health_router)
router.include_router(users_router)
router.include_router(auth_router)
router.include_router(category_router)
router.include_router(style_router)

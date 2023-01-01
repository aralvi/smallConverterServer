from fastapi import APIRouter
from app.routes.user_routes import user_router
from app.routes.conversion_routes import conversion_router
from app.routes.document_routes import document_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["Users"])
router.include_router(
    conversion_router, prefix="/convert", tags=["Conversions"]
)
router.include_router(document_router, prefix="/documents", tags=["documents"])

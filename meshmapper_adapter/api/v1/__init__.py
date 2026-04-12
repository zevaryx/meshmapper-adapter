from fastapi import APIRouter
from .auth.router import router as auth_router
from .pings.router import router as ping_router
from .repeaters.router import router as repeater_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
router.include_router(ping_router)
router.include_router(repeater_router)

import logging

from fastapi import FastAPI

from vsm_restaurant.dependencies import lifespan

from .demo import router as demo_router
from .menu import public_router as menu_public_router, admin_router as menu_admin_router
from .ingredients import router as ingredients_admin_router

logger = logging.getLogger(__name__)

media_location_prefix = "/media/"
app = FastAPI(lifespan=lifespan)

app.include_router(demo_router)
app.include_router(menu_public_router)
app.include_router(menu_admin_router)
app.include_router(ingredients_admin_router)

@app.get("/")
async def root():
    return "Hello world"


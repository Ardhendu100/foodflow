from fastapi import FastAPI

from foodflow.api.v1.auth import router as auth_router
from foodflow.api.v1.restaurant import router as restaurant_router
from foodflow.api.v1.menu import router as menu_router

app = FastAPI(
    title="FoodFlow API",
)

app.include_router(auth_router)
app.include_router(restaurant_router)
app.include_router(menu_router)

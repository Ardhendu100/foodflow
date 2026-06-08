from fastapi import FastAPI

from foodflow.api.v1.auth import router as auth_router

app = FastAPI(
    title="FoodFlow API",
)

app.include_router(auth_router)

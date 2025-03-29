from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.contacts import router as api_router
from app.views.views import router as views_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="api/static"), name="static")

app.include_router(views_router)
app.include_router(api_router, prefix="/api")
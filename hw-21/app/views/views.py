from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.api.contacts import contact_book

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/")
async def index(request: Request):
    """
    Главная страница: отображает список контактов.
    """
    contacts = contact_book.get_all_contacts()
    return templates.TemplateResponse("index.html", {"request": request, "contacts": contacts})

@router.get("/about/")
async def about(request: Request):
    """
    Страница "О сайте".
    """
    return templates.TemplateResponse("about.html", {"request": request})
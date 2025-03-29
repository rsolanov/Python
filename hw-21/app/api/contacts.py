from fastapi import APIRouter, HTTPException, Query
from app.models.contact import Contact, ContactBook
from app.utils.file_handler import FileHandler
from app.exceptions import ContactAlreadyExistsError, ContactNotFoundError
import logging

router = APIRouter()
contact_book = ContactBook()
file_handler = FileHandler()
FILE_NAME = "contact_book.json"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.on_event("startup")
async def load_contacts():
    """
    Загрузка контактов из файла при запуске приложения.
    """
    try:
        contacts = file_handler.load_contacts(FILE_NAME)

        contact_book.contacts.clear()

        for contact in contacts.values():
            contact_book.contacts[contact.phone] = contact
        logger.info("Contacts loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading contacts: {e}")


@router.on_event("shutdown")
async def save_contacts():
    """
    Сохранение контактов в файл при завершении работы приложения.
    """
    try:
        file_handler.save_contacts(FILE_NAME, contact_book.get_all_contacts())
        logger.info("Contacts saved successfully.")
    except Exception as e:
        logger.error(f"Error saving contacts: {e}")


@router.get("/contacts/")
async def get_contacts():
    """
    Возвращает список всех контактов.
    """
    return contact_book.get_all_contacts()


@router.post("/contacts/")
async def add_contact(
        phone: str,
        name: str,
        email: str
):
    """
    Добавляет новый контакт.
    """
    try:
        new_contact = Contact(name=name, phone=phone, email=email)
        contact_book.add_contact(new_contact)
        return {"message": "Contact added successfully."}
    except ContactAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/contacts/{phone}")
async def edit_contact(
        phone: str,
        name: str,
        email: str
):
    """
    Редактирует существующий контакт.
    """
    try:
        contact = contact_book.find_contact(phone)
        if not contact:
            raise ContactNotFoundError(f"Contact with phone {phone} not found.")

        if name:
            contact.name = name
        if email:
            contact.email = email

        return {"message": "Contact updated successfully."}
    except ContactNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/contacts/{phone}")
async def delete_contact(phone: str):
    """
    Удаляет контакт.
    """
    try:
        contact_book.delete_contact(phone)
        return {"message": "Contact deleted successfully."}
    except ContactNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/contacts/search/")
async def search_contact(
        phone: str = Query(None, description="Phone number to search"),
        name: str = Query(None, description="Name to search")
):
    """
    Ищет контакт по номеру телефона или имени.
    """
    try:
        if phone:
            contact = contact_book.find_contact(phone)
            if not contact:
                raise ContactNotFoundError(f"Contact with phone {phone} not found.")
            return contact
        elif name:
            results = [
                contact for contact in contact_book.get_all_contacts().values()
                if name.lower() in contact.name.lower()
            ]
            if not results:
                raise ContactNotFoundError(f"No contacts found with name {name}.")
            return results
        else:
            raise HTTPException(status_code=400, detail="Please provide a phone or name to search.")
    except ContactNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
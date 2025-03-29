from pydantic import BaseModel
from app.exceptions import ContactAlreadyExistsError, ContactNotFoundError

class Contact(BaseModel):
    name: str
    phone: str
    email: str

class ContactBook:
    def __init__(self):
        self.contacts = {}

    def add_contact(self, contact: Contact) -> None:
        if contact.phone in self.contacts:
            raise ContactAlreadyExistsError(f"Contact with phone {contact.phone} already exists.")
        self.contacts[contact.phone] = contact

    def find_contact(self, phone: str) -> Contact | None:
        return self.contacts.get(phone)

    def edit_contact(self, phone: str, name: str, email: str) -> None:
        contact = self.find_contact(phone)
        if not contact:
            raise ContactNotFoundError(f"Contact with phone {phone} not found.")
        contact.name = name
        contact.email = email
  
    def delete_contact(self, phone: str) -> None:
        if phone not in self.contacts:
            raise ContactNotFoundError(f"Contact with phone {phone} not found.")
        del self.contacts[phone]

    def get_all_contacts(self) -> dict[str, Contact]:
        return self.contacts
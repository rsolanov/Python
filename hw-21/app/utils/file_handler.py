import json
import os
from app.models.contact import Contact
from app.exceptions import InvalidDataFormatError

class FileHandler:
    @staticmethod
    def load_contacts(filename: str) -> dict[str, Contact]:
        """
        Загрузка контактов из файла.
        """
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                raise InvalidDataFormatError("Invalid JSON format in file.")

            contacts = {}
            for phone, info in data.items():
                if isinstance(info, list) and len(info) == 2:
                    name, email = info
                    contacts[phone] = Contact(name=name, phone=phone, email=email)
                else:
                    raise InvalidDataFormatError(f"Invalid data format for contact with phone {phone}.")
            return contacts
        return {}

    @staticmethod
    def save_contacts(filename: str, contacts: dict[str, Contact]) -> None:
        """
        Сохранение контактов в файл.
        """
        data_to_save = {
            contact.phone: [contact.name, contact.email]
            for contact in contacts.values()
        }
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data_to_save, file, indent=2, ensure_ascii=False)
import datetime
import re

class Field:
    def __init__(self):
        self._value = None

    #getter
    def value(self):
        return self._value

    #setter
    def value(self, new_value):
        self._value = new_value


class Phone(Field): #перевірка на п-сть для поля phone
    def value(self, new_value):
        if self._is_valid_phone(new_value):
            self._value = new_value
        else:
            raise ValueError("Invalid phone number")

    def _is_valid_phone(self, phone): # Перевірка на коректність номера телефону
        if phone.startswith("+380") and len(phone) == 13 and phone[4:].isdigit():
            return True
        else:
            return False

users = {
    "Viktoriia": "30.08.1999",
    "Edhar": "14.08.1996",
    "Aleksandr": "31.07.1970",
    "Tatiana": "01.08.1979"
}

class Birthday(Field): #перевірка на п-сть для поля birthday
    DATE_PATTERN = r"^\d{2}\.\d{2}\.\d{4}$"
    
    def _is_valid_birthday(self, birthday): # Перевірка на коректність дня народження
        if re.match(self.DATE_PATTERN, birthday) and birthday in users.values():
            return birthday
        return None
    
    def value(self, new_value):
        valid_birthday = self._valid_birthday(new_value)
        if valid_birthday:
            self._value = valid_birthday
        else:
            raise ValueError("Invalid birthday")


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phone = phone
        self.birthday = birthday

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.date.today()
            next_birthday = datetime.date(today.year, self.birthday.value.month, self.birthday.value.day)
            if today > next_birthday:
                next_birthday = datetime.date(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            days = (next_birthday - today).days
            return days
        else:
            return None


class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def remove_record(self, record):
        self.records.remove(record)

    def __iter__(self):
        return iter(self.records)

    def get_records(self, page_number, page_size):
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        return self.records[start_index:end_index]


# Пример использования классов и методов

# Создаем экземпляры записей
record1 = Record("John Doe", Phone(), Birthday())
record1.phone.value = "1234567890"
record1.birthday.value = datetime.date(1990, 5, 10)

record2 = Record("Jane Smith", Phone(), Birthday())
record2.phone.value = "9876543210"
record2.birthday.value = datetime.date(1985, 10, 20)

# екземпляр адресної книги
address_book = AddressBook()

# додаємо записи
address_book.add_record(record1)
address_book.add_record(record2)

# к-сть днів до д.р.
for record in address_book:
    days = record.days_to_birthday()
    if days is not None:
        print(f"Days to birthday for {record.name}: {days}")
    else:
        print(f"No birthday set for {record.name}")

# пагінаця
page_number = 1
page_size = 1
records = address_book.get_records(page_number, page_size)
for record in records:
    print(record.name, record.phone.value, record.birthday.value)

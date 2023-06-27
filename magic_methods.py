import datetime
import re

class Field:
    def __init__(self):
        self._value = None

    #getter
    def get_value(self):
        return self._value

    #setter
    def set_value(self, new_value):
        self._value = new_value


class Phone(Field): #перевірка на п-сть для поля phone
    def set_value(self, new_value):
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
    
    def set_value(self, new_value):
        valid_birthday = self._is_valid_birthday(new_value)
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


class AddressBook: # пагінація #метод iterator, який за одну ітерацію повертає представлення для N записів
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def remove_record(self, record):
        self.records.remove(record)

    def __iter__(self):
        return self.iterator()

    def iterator(self, n=1):
        count = 0
        current_index = 0

        while count < len(self.records):
            if current_index >= len(self.records):
                current_index = 0
            yield self.records[current_index]
            count += 1
            current_index += 1

            if count % n == 0:
                break

    def get_records(self, page_number, page_size):
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        return self.records[start_index:end_index]

from collections import UserDict
import pickle #б.для серіалізації/десеріалізації

class AddressBook(UserDict): #Клас AddressBook, який наслідується від UserDict
    def add_record(self, record):
        self.data[record.id] = record

    def search_by_name(self, name): #логіка пошуку за записами
        matching_records = []
        for key in self.data:
            record = self.data[key]
            if record.name == name:
                matching_records.append(record)
        return matching_records
    
    def search_by_phone(self, phone): #логіка пошуку за н.телефону
        matching_records = []
        for record in self.data.values():
            for phone_obj in record.phones:
                if phone in phone_obj.value:
                    matching_records.append(record)
                    break
        return matching_records

    def save_to_file(self, filename):  #збереження адресної книги у файл
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename): #файл з якого буде відновлено адресну книгу
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            pass


class Field: # батьківський клас для всіх полів
    def __init__(self, value):
        self.value = value


class Name(Field): #обов'язкове поле з ім'ям
    pass


class Phone(Field): #необов'язкове поле з телефоном
    pass


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]


address_book = AddressBook() #екземпляр классу AddressBook


def add_contact(name, phone): #додавання контакту
    record = Record(name)
    record.add_phone(phone)
    address_book.add_record(record)
    return "Контакт додано: {} - {}".format(name, phone)


def delete_contact(name): #видалення контакту
    matching_records = address_book.search_by_name(name)
    if matching_records:
        record = matching_records[0]
        del address_book.data[record.name.value]
        return "Контакт видалено: {} - {}".format(name, record.phones)
    else:
        return "Контакт не знайдено: {}".format(name)


def change_contact_handler(name, new_phone): #змінення контакту
    matching_records = address_book.search_by_name(name)
    if matching_records:
        record = matching_records[0]
        old_phone = record.phones[0].value
        record.remove_phone(old_phone)
        record.add_phone(new_phone)
        return "Контакт редаговано: {} - {} (old phone: {})".format(name, new_phone, old_phone)
    else:
        return "Контакт не знайдено: {}".format(name)
    
def search_contacts(query): #пошук контактів за запитом
    matching_records = address_book.search_by_name(query) + address_book.search_by_phone(query)
    if matching_records:
        result = "Matching contacts:\n"
        for record in matching_records:
            result += "{} - {}\n".format(record.name.value, ", ".join([phone.value for phone in record.phones]))
        return result.strip()
    else:
        return "No matching contacts found."

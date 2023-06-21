from collections import UserDict


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

import re
import pickle
from datetime import date, datetime
from collections import UserDict


class Field:
    def __init__(self, value=None):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value):
        pass


class Name(Field):
    pass


class Phone(Field):
    PHONE_REGEX = re.compile(r"^\+?(\d{2})?\(?\d{3}\)?[\d\-\s]{7,10}$")

    def validate(self, phone):
        if not self.PHONE_REGEX.match(phone):
            raise ValueError(f"Phone number {phone} is invalid.")

    @property
    def value(self):
        if self._value:
            return self._value
        return None

    @value.setter
    def value(self, new_value):
        while True:
            try:
                self.validate(new_value)
                self._value = new_value
                break
            except ValueError:
                new_value = input("Please enter phone number in proper format(380*********): ")


class Address(Field):
    pass


class Birthday(Field):
    DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    def validate(self, date_str):
        if not self.DATE_REGEX.match(date_str):
            raise ValueError(f"Invalid date format: {date_str}. Expected format: YYYY-MM-DD.")
        year, month, day = map(int, date_str.split('-'))
        if month > 12 or year > 2023 or day > 31:
            raise ValueError(f"Invalid month: {month}. Month should be between 1 and 12.")

    @property
    def value(self):
        if self._value:
            return datetime.strptime(self._value, "%Y-%m-%d").date()
        return None

    @value.setter
    def value(self, new_value):
        while True:
            try:
                self.validate(new_value)
                self._value = new_value
                break
            except ValueError:
                new_value = input("Please enter the birthday in the format YYYY-MM-DD: ")


class Email(Field):
    EMAIL_REGEX = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")

    def validate(self, email_str):
        if not self.EMAIL_REGEX.match(email_str):
            raise ValueError(f"Invalid email")

    @property
    def value(self):
        if self._value:
            return self._value
        return None

    @value.setter
    def value(self, new_value):
        while True:
            try:
                self.validate(new_value)
                self._value = new_value
                break
            except ValueError:
                new_value = input("Please enter a valid email: ")


class Record:
    def __init__(self, name, address=None, birthday=None, email=None):
        self.name = name
        self.phones = []
        self.address = address
        self.birthday = birthday
        self.email = email

    def add(self, phone):
        self.phones.append(phone)

    def set_birthday(self, birthday):
        self.birthday = birthday

    def set_email(self, email):
        self.email = email

    def set_address(self, address):
        self.address = address

    def days_to_birthday(self):
        if self.birthday and self.birthday.value:
            today = date.today()
            next_birthday = date(today.year, self.birthday.value.month, self.birthday.value.day)
            if today > next_birthday:
                next_birthday = date(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            days_left = (next_birthday - today).days
            return days_left
        return None


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, name):
        self.data.pop(name, None)

    def get_all_records(self):
        return self.data.values()


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except (IndexError, ValueError):
            return "Input Error.Please try one more time."
        except KeyError:
            return "No such contact, please try one more time."
    return inner


class Assistant:
    SAVE_FILE = "address_book.pickle"

    def __init__(self):
        self.address_book = AddressBook()

    @input_error
    def create(self):
        name = input("Write name: ")
        record = Record(Name(name))
        phone = input("Enter phone number: ")
        if phone:
            record.add(Phone(phone))
        address = input("Enter address: ")
        if address:
            record.set_address(Address(address))
        birthday = input("Please enter birthday (Format: YYYY-MM-DD): ")
        if birthday:
            record.set_birthday(Birthday(birthday))
        email = input("Please enter email:")
        if email:
            record.set_email(Email(email))
        self.address_book.add_record(record)
        return "Contact was added."

    @input_error
    def add(self):
        name = input("Please enter name of person to which you are willing to add info:")
        record = self.address_book.data.get(name)
        if not record:
            return "No such contact - please check your input."
        extra = input("What we are willing to add?(Phone, Address, Birthday, Email):").lower()
        if extra == 'phone':
            phone = input('Please enter extra phone:')
            record.add(Phone(phone))
            return "Phone was added"
        if extra == 'address':
            address = input('Please enter Address:')
            record.set_address(Address(address))
            return "Address was added"
        if extra == 'birthday':
            birthday = input('Please enter Birthday:')
            record.set_birthday(Birthday(birthday))
            return "Birthday was added"
        if extra == 'email':
            email = input('Please enter Email:')
            record.set_email(Email(email))
            return "Email was added"

    @input_error
    def change(self):
        name = input("Please enter name of person:")
        record = self.address_book.data.get(name)
        if not record:
            return "No such contact with phone number."
        extra = input("What we are willing to change?(Phone, Address, Birthday, Email):").lower()
        if extra == 'phone':
            phone = input('Please enter new phone:')
            record.phones = [Phone(phone)]
            return "Phone was changed"
        if extra == 'address':
            address = input('Please new Address:')
            record.set_address(Address(address))
            return "Address was changed"
        if extra == 'birthday':
            birthday = input('Please enter Birthday:')
            record.set_birthday(Birthday(birthday))
            return "Birthday was changed"
        if extra == 'email':
            email = input('Please enter Email:')
            record.set_email(Email(email))
            return "Email was changed"

    @input_error
    def phone(self):
        name = input("Please enter name of person:")
        record = self.address_book.data.get(name)
        if not record:
            return "No such contact with this phone number."
        return ', '.join([str(phone.value) for phone in record.phones])

    def show(self):
        return "\n".join([str(record.name.value) + ": "
                          + ', '.join([str(phone.value) for phone in record.phones])
                          + (f", Address: {record.address.value}" if record.address else ", [No Address] ")
                          + (f", Email: {record.email.value}" if record.email else ", [No Email] ")
                          + (f", Birthday: {record.birthday.value}" if record.birthday else ", [No Birthday]")
                          for record in self.address_book.get_all_records()])

    @input_error
    def birthday(self):
        name = input("Please enter name of person:")
        record = self.address_book.data.get(name)
        if not record:
            return "No such contact with this name."
        days = record.days_to_birthday()
        if days:
            return f"{days} left till birthday."
        else:
            return "There is no birthday day."

    def whom(self):
        days = int(input("Please enter for how many days you are looking for:"))
        upcoming_birthday_contacts = [
            record.name.value + f' Was born:{record.birthday.value}'
            for record in self.address_book.get_all_records()
            if record.days_to_birthday() in range(0, days)
        ]
        if upcoming_birthday_contacts:
            return f"Contacts with upcoming birthday in {days} days:\n" + "\n".join(upcoming_birthday_contacts)
        else:
            return f"No contacts with upcoming birthday in {days} days."

    def search(self):
        query = input("Please enter what we are looking for:")
        for record in self.address_book.values():
            if query.lower() in record.name.value.lower() or any(query in phone.value for phone in record.phones):
                return "\n".join([str(record.name.value) + ": "
                                  + ', '.join([str(phone.value) for phone in record.phones])
                                  + (f", Address: {record.address.value}" if record.address else ", [No Address] ")
                                  + (f", Email: {record.email.value}" if record.email else ", [No Email] ")
                                  + (f", Birthday: {record.birthday.value}" if record.birthday else ", [No Birthday]")
                                  for record in self.address_book.get_all_records()])

    def delete(self):
        name = input("Please enter name of contact that you are willing to delete:")
        record = self.address_book.data.get(name)
        if not record:
            return "No such contact with this name."
        self.address_book.remove_record(name)
        return "Contact was deleted"

    @input_error
    def exit(self):
        self.save()
        return "See you in Assistant!"

    def load_data(self):
        try:
            with open(self.SAVE_FILE, "rb") as file:
                self.address_book = pickle.load(file)
        except FileNotFoundError:
            pass

    def save(self):
        with open(self.SAVE_FILE, "wb") as file:
            pickle.dump(self.address_book, file)
        return "Was saved!"


def run_assistant():
    assistant = Assistant()
    assistant.load_data()
    print("Welcome to Assistant! I know such commands:\n"
          "Create - Create new Person to Contacts\n"
          "Add - Add extra info to Contact\n"
          "Change - Changing existing phone for contact \n"
          "Phone - Showing phone for person\n"
          "Show - Show all contacts in AddressBook\n"
          "Birthday - How many days till Birthday \n"
          "Whom - Who is celebrating birthday in next days\n"
          "Save - Saving all info\n"
          "Delete - Deleting contact from Addressbook\n"
          "Exit - Close Assistant \n")
    while True:
        print("Commands: Create, Add, Change, Phone, Show, Birthday, Whom, Save, Delete, Exit")
        command = input(">>> ")
        function = getattr(assistant, command.lower().strip(), None)
        if function:
            print(function())
        else:
            print("Unknown command - please try one more time.")
        if command == 'exit':
            break


if __name__ == "__main__":
    run_assistant()
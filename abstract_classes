import re
import pickle
from datetime import date, datetime
from collections import UserDict
from abc import ABC, abstractmethod

# Define Field, Name, Phone, Address, Birthday, Email, Record, AddressBook, InputError classes (same as before)

class DisplayStrategy(ABC):
    @abstractmethod
    def display(self, content):
        pass

class ConsoleDisplayStrategy(DisplayStrategy):
    def display(self, content):
        for item in content:
            print(item)

class CardDisplayStrategy(DisplayStrategy):
    def display(self, content):
        for item in content:
            print(f"---\n{item}\n---\n")

class NoteDisplayStrategy(DisplayStrategy):
    def display(self, content):
        for item in content:
            print(f"Note:\n{item}\n")

class Assistant:
    SAVE_FILE = "address_book.pickle"

    def __init__(self, display_strategy):
        self.address_book = AddressBook()
        self.display_strategy = display_strategy

    def run(self):
        self.load_data()
        self.display_welcome_message()

        while True:
            command = self.get_user_input("Enter a command: ")
            if command.lower() == "exit":
                self.save_data()
                break

            try:
                self.execute_command(command)
            except InputError as e:
                print(f"Input Error: {e}")
            except KeyError:
                print("No such contact, please try again.")

    def display_welcome_message(self):
        print("Welcome to Assistant! Available commands:")
        print("Create - Create a new contact")
        print("Add - Add additional information to a contact")
        print("Change - Change existing information for a contact")
        print("Phone - Display phone number for a contact")
        print("Show - Display all contacts")
        print("Birthday - Show days left until a contact's birthday")
        print("Whom - Show contacts with upcoming birthdays")
        print("Delete - Delete a contact")
        print("Exit - Save data and exit")

    def execute_command(self, command):
        command = command.lower().strip()
        if command == "create":
            self.create()
        elif command == "add":
            self.add()
        elif command == "change":
            self.change()
        elif command == "phone":
            self.phone()
        elif command == "show":
            self.show()
        elif command == "birthday":
            self.birthday()
        elif command == "whom":
            self.whom()
        elif command == "delete":
            self.delete()
        else:
            raise InputError("Unknown command. Please try again.")

    def create(self):
        # Implementation for the create method
        pass

    def add(self):
        # Implementation for the add method
        pass

    def change(self):
        name = self.get_user_input("Enter name of the person to change information: ")
        record = self.address_book.data.get(name)
        if not record:
            raise InputError("No such contact - please check your input.")
        extra = self.get_user_input("What information would you like to change? (Phone, Address, Birthday, Email): ").lower()
        if extra == 'phone':
            phone = self.get_user_input("Please enter new phone: ")
            record.phones = [Phone(phone)]
            print("Phone was changed.")
        elif extra == 'address':
            address = self.get_user_input("Please enter new Address: ")
            record.set_address(Address(address))
            print("Address was changed.")
        elif extra == 'birthday':
            birthday = self.get_user_input("Please enter new Birthday: ")
            record.set_birthday(Birthday(birthday))
            print("Birthday was changed.")
        elif extra == 'email':
            email = self.get_user_input("Please enter new Email: ")
            record.set_email(Email(email))
            print("Email was changed.")
        else:
            raise InputError("Unknown information type. Please try again.")

    def phone(self):
        name = self.get_user_input("Enter name of the person to display phone number: ")
        record = self.address_book.data.get(name)
        if not record:
            raise InputError("No such contact - please check your input.")
        if not record.phones:
            print("No phone number available.")
        else:
            print("Phone numbers:")
            for phone in record.phones:
                print(phone.value)

    def show(self):
        records = self.get_formatted_records()
        self.display_strategy.display(records)

    def birthday(self):
        name = self.get_user_input("Enter name of the person to show birthday: ")
        record = self.address_book.data.get(name)
        if not record:
            raise InputError("No such contact - please check your input.")
        if not record.birthday:
            print("Birthday information is not available.")
        else:
            days_left = record.days_to_birthday()
            if days_left is None:
                print("Birthday is today!")
            else:
                print(f"Days left until birthday: {days_left}")

    def whom(self):
        # Implementation for the whom method
        pass

    def delete(self):
        name = self.get_user_input("Enter name of the person to delete: ")
        if name in self.address_book.data:
            self.address_book.remove_record(name)
            print("Contact deleted.")
        else:
            print("Contact not found.")

    def get_formatted_records(self):
        # Implementation for formatting records
        pass

    def get_user_input(self, prompt):
        return input(prompt)

    def load_data(self):
        try:
            with open(self.SAVE_FILE, "rb") as file:
                self.address_book = pickle.load(file)
        except FileNotFoundError:
            pass

    def save_data(self):
        with open(self.SAVE_FILE, "wb") as file:
            pickle.dump(self.address_book, file)
        print("Data was saved.")

def run_assistant():
    console_display = ConsoleDisplayStrategy()
    assistant = Assistant(console_display)
    assistant.run()

if __name__ == "__main__":
    run_assistant()

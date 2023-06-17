contacts = {}

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Invalid command. Please try again."
        except ValueError:
            return "Invalid value. Please try again."
        except IndexError:
            return "Index out of range. Please try again."
    return wrapper

def parse_command(user_input):
    keywords = user_input.lower().split()
    return keywords

@input_error
def add_contact_handler():
    name, phone = input("Enter the name and phone number: ").split()
    contacts[name] = phone
    return "Contact added: {} - {}".format(name, phone)

@input_error
def change_contact_handler():
    name, phone = input("Enter the name and new phone number: ").split()
    if name in contacts:
        contacts[name] = phone
        return "Contact updated: {} - {}".format(name, phone)
    else:
        return "Contact not found. Please try again."

@input_error
def phone_contact_handler():
    name = input("Enter the name of the contact: ")
    if name in contacts:
        return "Phone number: {}".format(contacts[name])
    else:
        return "Contact not found. Please try again."

@input_error
def show_all_handler():
    if contacts:
        all_contacts = "\n".join(["{} - {}".format(name, phone) for name, phone in contacts.items()])
        return "All contacts:\n{}".format(all_contacts)
    else:
        return "No contacts found."

def main():
    while True:
        user_input = input("Enter a command: ")
        keywords = parse_command(user_input)

        if "hello" in keywords:
            print("How can I help you?")
        elif "add" in keywords and "contact" in keywords:
            print(add_contact_handler())
        elif "change" in keywords and "contact" in keywords:
            print(change_contact_handler())
        elif "phone" in keywords and "contact" in keywords:
            print(phone_contact_handler())
        elif "show" in keywords and "all" in keywords:
            print(show_all_handler())
        elif any(keyword in keywords for keyword in ["good", "bye", "close", "exit"]):
            print("Good bye!")
            break
        else:
            print("Unknown command. Please try again.")

main()
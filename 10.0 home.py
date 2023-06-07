from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    pass

class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except KeyError:
            result = "No user with given name"
        except ValueError:
            result = "Give me name and phone please"
        except IndexError:
            result = "Enter user name"
        return result
    return inner

def hello_handler():
    return "How can I help you?"

def add_handler(command):
    name, phone = command.split()[1:]
    name = Name(name)
    phone = Phone(phone)
    record = Record(name)
    record.add_phone(phone)
    address_book.add_record(record)
    return f"User {name.value} with phone number {phone.value} was added"

def change_handler(command):
    name, phone = command.split()[1:]
    name = Name(name)
    phone = Phone(phone)
    record = address_book.data[name.value]
    old_phone = record.phones[0]
    record.edit_phone(old_phone, phone)
    return f"Phone number for user {name.value} was changed to {phone.value}"

def phone_handler(command):
    name = command.split()[1]
    name = Name(name)
    record = address_book.data[name.value]
    phones = [phone.value for phone in record.phones]
    return "\\n".join(phones)

def show_all_handler():
    result = []
    for name, record in address_book.data.items():
        phones = [phone.value for phone in record.phones]
        result.append(f"{name}: {', '.join(phones)}")
    return "\\n".join(result)

def exit_handler():
    return "Good bye!"

HANDLERS = {
    "hello": hello_handler,
    "add": add_handler,
    "change": change_handler,
    "phone": phone_handler,
    "show all": show_all_handler,
    "good bye": exit_handler,
    "close": exit_handler,
    "exit": exit_handler
}

address_book = AddressBook()

@input_error
def handle_command(command):
    command = command.lower()
    for key in HANDLERS:
        if command.startswith(key):
            handler = HANDLERS[key]
            return handler(command)
    return "Unknown command"

def main():
    while True:
        command = input()
        result = handle_command(command)
        print(result)
        if result == "Good bye!":
            break

if __name__ == "__main__":

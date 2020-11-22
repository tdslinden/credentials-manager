from database_manager import insert_credentials, update_credentials, get_credentials, delete_credentials
import config
import random


def check_if_length_valid(length):
    max_length = 15
    min_length = 8
    try:
        length = int(length)
        if max_length >= length >= min_length:
            return True
    except ValueError:
        print("Length must be a value between 8 and 15 inclusive.")

    return False


def generate_password():
    command = "\nEnter length of password (8 - 15): "
    length = input(command)
    is_valid_entry = check_if_length_valid(length)

    while not is_valid_entry:
        length = input(command)
        is_valid_entry = check_if_length_valid(length)

    length = int(length)
    chars = "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*."
    generated_password = ""
    for i in range(length):
        generated_password += random.choice(chars)
    print("Generated password: " + generated_password)


def menu():
    commands = "\n" \
               "------------------------------\n" \
               "What would you like to do?\n" \
               "------------------------------\n" \
               "i: Insert New Credentials\n" \
               "u: Update Existing Credentials\n" \
               "g: Get Credentials\n" \
               "p: Generate Password\n" \
               "d: Delete Credentials\n" \
               "q: Quit Program\n" \
               "------------------------------\n" \
               ": "

    command = input(commands)

    while command != "q":
        if command == "i":
            insert_credentials()
        elif command == "u":
            update_credentials()
        elif command == "g":
            get_credentials()
        elif command == "p":
            generate_password()
        else:
            delete_credentials()

        command = input(commands)


def run_insert_prompt():
    username = input("\nEnter username: ")
    password = input("Enter password: ")
    platform = input("Enter platform (e.g. Facebook): ")
    return username, password, platform


def run_update_prompt():
    username = input("\nEnter the username you would like to update: ")
    platform = input("Enter the platform the username is associated to: ")

    select_credentials_query = ("SELECT count(1) FROM credentials where username = '{}' AND"
                                " platform = '{}'").format(username, platform)

    cursor = connector.cursor(buffered=True)
    cursor.execute(select_credentials_query)

    if not cursor:
        raise Exception

    command = input("\n"
                    "------------------------------\n"
                    "What would you like to update?\n"
                    "------------------------------\n"
                    "u: Username\n"
                    "p: Password\n"
                    "b: Both Username and Password\n"
                    "------------------------------\n"
                    ": ")

    new_username = ""
    new_password = ""
    if command == "p":
        new_password = input("Enter new password: ")
        confirmation_password = input("Confirm new password: ")
        while new_password != confirmation_password:
            new_password = input("Enter new password: ")
            confirmation_password = input("Confirm new password: ")
    elif command == "u":
        new_username = input("Enter new username:")
        confirmation_username = input("Enter new username:")
        while new_username != confirmation_username:
            new_username = input("Enter new username:")
            confirmation_username = input("Confirm new username:")
    elif command == "b":
        new_username = input("Enter new username:")
        confirmation_username = input("Enter new username:")
        while new_username != confirmation_username:
            new_username = input("Enter new username:")
            confirmation_username = input("Confirm new username:")
        new_password = input("Enter new password: ")
        confirmation_password = input("Confirm new password: ")
        while new_password != confirmation_password:
            new_password = input("Enter new password: ")
            confirmation_password = input("Confirm new password: ")

    return new_username, new_password, username, platform


def run_get_prompt():
    command = input("\n"
                    "------------------------------\n"
                    "What would you like to do?\n"
                    "------------------------------\n"
                    "1. Get all credentials.\n"
                    "2. Get credentials based on platform.\n"
                    "------------------------------\n"
                    ":"
                    )

    if command == '2':
        platform = input("\nEnter the platform: ")
        return platform

    return "all"


def run_delete_prompt():
    command = input("\n"
                    "------------------------------\n"
                    "What would you like to do?\n"
                    "------------------------------\n"
                    "1. Delete specific credentials.\n"
                    "2. Delete all credentials.\n"
                    "------------------------------\n"
                    ":"
                    )

    username = "all"
    platform = "all"
    if command == "1":
        username = input("\nEnter the username of the credentials you would like to delete: ")
        platform = input("Enter the platform the username is associated to: ")
    elif command == "2":
        confirmation = input("Are you sure (y/n)? \n"
                             ":")

        if confirmation == "n":
            delete_credentials()

    return username, platform


def run_password_manager():
    print(('-' * 13) + 'Password Manager' + ('-' * 13))
    password = input("Enter password: ")

    correct_password = config.master_password
    while password != correct_password:
        password = input("Incorrect Password\nEnter password: ")

    print("Log In Successful")

    menu()
    exit()


if __name__ == '__main__':
    run_password_manager()

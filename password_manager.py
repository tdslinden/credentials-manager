from database_manager import insert_credentials, update_credentials, get_credentials, delete_credentials, check_credentials
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
            run_insert_prompt()
        elif command == "u":
            run_update_prompt()
        elif command == "g":
            run_get_prompt()
        elif command == "p":
            generate_password()
        else:
            run_delete_prompt()

        command = input(commands)


def run_insert_prompt():
    username = input("\nEnter username: ")
    password = input("Enter password: ")
    platform = input("Enter platform (e.g. Facebook): ")
    insert_credentials(username, password, platform)


def run_update_prompt():
    username = input("\nEnter the username you would like to update: ")
    platform = input("Enter the platform the username is associated to: ")

    credentials_exist = check_credentials(username, platform)

    if credentials_exist:
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

        update_credentials(new_username, new_password, username, platform)
        print("\nUpdate Successful!")
    else:
        print("The account associated with the username and platform does not exist")


def run_get_prompt():
    command = input("\n"
                    "------------------------------\n"
                    "What would you like to do?\n"
                    "------------------------------\n"
                    "1. Get all credentials.\n"
                    "2. Get credentials based on platform.\n"
                    "------------------------------\n"
                    ": "
                    )

    platform = 'all'
    if command == '2':
        platform = input("\nEnter the platform: ")
    credentials = get_credentials(platform)

    if credentials:
        number_of_dashes = 86
        print("\n" + '-' * number_of_dashes)
        print(('-' * 40) + "Result" + ('-' * 40))
        for credential in credentials:
            username = credential['username']
            password = credential['password']
            platform = credential['platform']
            print('-' * number_of_dashes)
            print("Username: {:<20} | Password: {:<15} | Platform: {:<10}".format(username, password, platform))
        print('-' * number_of_dashes)
    else:
        print("\n No Saved Credentials.")


def run_delete_prompt():
    command = input("\n"
                    "------------------------------\n"
                    "What would you like to do?\n"
                    "------------------------------\n"
                    "1. Delete specific credentials.\n"
                    "2. Delete all credentials.\n"
                    "------------------------------\n"
                    ": "
                    )

    if command == "1":
        username = input("\nEnter the username of the credentials you would like to delete: ")
        platform = input("Enter the platform the username is associated to: ")
        delete_credentials(username=username, platform=platform)
        print("\nDelete Successful!")
    elif command == "2":
        confirmation = input("Are you sure (y/n)? \n"
                             ":")

        if confirmation == "y":
            delete_credentials()
            print("\nDelete Successful!")


def run_password_manager():
    print(('-' * 13) + 'Password Manager' + ('-' * 13))
    password = input("Enter password: ")

    correct_password = config.master_password
    while password != correct_password:
        password = input("Incorrect Password\nEnter password: ")

    print("\nLog In Successful!")

    menu()
    exit()


if __name__ == '__main__':
    run_password_manager()

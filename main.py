import mysql.connector
import config
from mysql.connector import errorcode
from datetime import date, datetime, timedelta

commands = "\n" \
           "------------------------------\n" \
           "What would you like to do?\n" \
           "------------------------------\n" \
           "i: Insert New Credentials\n" \
           "u: Update Current Credentials\n" \
           "g: Get Credentials\n" \
           "p: Generate Password\n" \
           "d: Delete Credentials\n" \
           "q: Quit Program\n" \
           "------------------------------\n" \
           ": "


def check_master_password(password):
    correct_password = config.master_password
    while password != correct_password:
        password = input("Incorrect Password\nEnter password: ")


def run_mysql():
    try:
        connector = mysql.connector.connect(user=config.user,
                                            password=config.password,
                                            host=config.host,
                                            database=config.database)

        create_tables(connector)
        command = input(commands)

        while command != "q":
            if command == "i":
                insert_credentials(connector)
            elif command == "u":
                update_credentials(connector)
            elif command == "g":
                get_credentials(connector)
            elif command == "p":
                generate_password()
            elif command == "d":
                delete_credentials()

            command = input(commands)

        connector.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Incorrect Credentials")
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database Does Not Exist")
        else:
            print(err)


def create_tables(connector):
    cursor = connector.cursor()

    TABLES = {}
    TABLES['credentials'] = "CREATE TABLE credentials " \
                            "(userId int(11) NOT NULL AUTO_INCREMENT," \
                            "username varchar(50) NOT NULL," \
                            "password varchar(15) NOT NULL," \
                            "platform varchar(15) NOT NULL," \
                            "created date NOT NULL," \
                            "lastUpdated date," \
                            "PRIMARY KEY (userId))"

    for table_name in TABLES:
        table_command = TABLES[table_name]
        try:
            cursor.execute(table_command)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table Already Exists.")
            else:
                print(err.msg)


def run_insert_prompt():
    username = input("\nEnter username: ")
    password = input("Enter password: ")
    platform = input("Enter platform (e.g. Facebook): ")
    return username, password, platform


def insert_credentials(connector):
    cursor = connector.cursor()
    today = datetime.now().date()

    insert_credentials_query = ("INSERT INTO credentials "
                                "(username, password, platform, created, lastUpdated) "
                                "VALUES (%s, %s, %s, %s, %s)")

    username, password, platform = run_insert_prompt()
    credentials_data = (username, password, platform, today, today)
    cursor.execute(insert_credentials_query, credentials_data)
    connector.commit()


def run_update_prompt(connector):
    username = input("\nEnter the username you would like to update: ")
    platform = input("Enter the platform the username is associated to: ")

    select_credentials_query = ("SELECT count(1) FROM credentials where username = '{}' AND"
                                " platform = '{}'").format(username, platform)

    cursor = connector.cursor(buffered=True)
    cursor.execute(select_credentials_query)

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


def update_credentials(connector):
    new_username, new_password, username, platform = run_update_prompt(connector)
    today = datetime.now().date()

    update_query = ""
    if new_password and not new_username:
        update_query = ("UPDATE credentials "
                        "SET password =  '{}', lastUpdated = '{}' "
                        "WHERE username = '{}' AND platform = '{}'").format(new_password, today, username, platform)
    elif new_username and not new_password:
        update_query = ("UPDATE credentials "
                        "SET username =  '{}', lastUpdated = '{}' "
                        "WHERE username = '{}' AND platform = '{}'").format(new_username, today, username, platform)
    elif new_username and new_password:
        update_query = ("UPDATE credentials "
                        "SET username =  '{}', password = '{}', lastUpdated = '{}' "
                        "WHERE username = '{}' AND platform = '{}'").format(new_username, new_password, today, username, platform)

    print(update_query)
    cursor = connector.cursor(buffered=True)
    cursor.execute(update_query)
    connector.commit()


def generate_password():
    x = 4


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


def get_credentials(connector):
    target_platform = run_get_prompt()
    cursor = connector.cursor()

    if target_platform == "all":
        get_all_credentials_query = "SELECT username, password, platform FROM credentials"
        cursor.execute(get_all_credentials_query)
    else:
        get_credentials_with_platform = "SELECT username, password, platform FROM credentials WHERE platform = '{}'".format(
            target_platform)
        cursor.execute(get_credentials_with_platform)

    print("\n--------------------------------------------------------------------------------\nCredentials")
    for (username, password, platform) in cursor:
        print("--------------------------------------------------------------------------------")
        print("Username: {:<20} | Password: {:<15} | Platform: {:<10}".format(username, password, platform))


def delete_credentials():
    x = 2


def main():
    print("~~~ Credentials Manager ~~~")
    password = input("Enter password: ")
    check_master_password(password)
    run_mysql()


if __name__ == '__main__':
    main()

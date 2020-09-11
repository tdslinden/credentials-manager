import mysql.connector
import config
from mysql.connector import errorcode


def check_master_password(password):
    correct_password = config.master_password
    while password != correct_password:
        # print("Incorrect Password")
        password = input("Incorrect Password \n Enter password: ")


def connect_to_mysql():
    try:
        connector = mysql.connector.connect(user=config.user,
                                            password=config.password,
                                            host=config.host,
                                            database=config.database)

        if connector.is_connected():
            db_info = connector.get_server_info()
            print(db_info)

        # do commands in here


        create_tables(connector)

        return connector

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Incorrect Credentials")
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def create_tables(connector):
    cursor = connector.cursor()

    TABLES = {}
    TABLES['credentials'] = "CREATE TABLE credentials " \
                            "(entry int PRIMARY KEY NOT NULL AUTO_INCREMENT, " \
                            "username varchar(50) NOT NULL," \
                            "password varchar(15) NOT NULL," \
                            "platform varchar(15) NOT NULL," \
                            "created date NOT NULL," \
                            "lastUpdated date)"

    for table_name in TABLES:
        table_command = TABLES[table_name]
        try:
            cursor.execute(table_command)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table already exists.")
            else:
                print(err.msg)


# might do update with insert
def insert_credentials():
    x = 4


def get_credentials():
    x = 2


def delete_credentials():
    x = 2


def main():
    print("~~~ Credentials Manager ~~~")
    password = input("Enter password: ")
    check_master_password(password)
    connector = connect_to_mysql()
    print("")

    connector.close()


if __name__ == '__main__':
    main()

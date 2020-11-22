import config
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime


def get_database_connector():
    try:
        connector = mysql.connector.connect(user=config.user,
                                            password=config.password,
                                            host=config.host,
                                            database=config.database,
                                            auth_plugin='mysql_native_password')

        return connector

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Incorrect Credentials")
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database Does Not Exist")
        else:
            print(err)


def create_tables(connector):
    cursor = connector.cursor()

    tables = {}
    tables['credentials'] = "CREATE TABLE credentials " \
                            "(userId int(11) NOT NULL AUTO_INCREMENT," \
                            "username varchar(50) NOT NULL," \
                            "password varchar(15) NOT NULL," \
                            "platform varchar(15) NOT NULL," \
                            "created date NOT NULL," \
                            "lastUpdated date," \
                            "PRIMARY KEY (userId))"

    for table_name in tables:
        table_command = tables[table_name]
        try:
            cursor.execute(table_command)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table Already Exists.")
            else:
                print(err.msg)


def insert_credentials(username, password, platform):
    connector = get_database_connector()
    cursor = connector.cursor()
    today = datetime.now().date()

    insert_credentials_query = ("INSERT INTO credentials "
                                "(username, password, platform, created, lastUpdated) "
                                "VALUES (%s, %s, %s, %s, %s)")

    credentials_data = (username, password, platform, today, today)
    cursor.execute(insert_credentials_query, credentials_data)
    connector.commit()
    connector.close()


def check_credentials(username, platform):
    connector = get_database_connector()
    cursor = connector.cursor(buffered=True)
    select_credentials_query = ("SELECT count(1) FROM credentials where username = '{}' AND"
                                " platform = '{}'").format(username, platform)
    cursor.execute(select_credentials_query)
    if cursor:
        return True
    else:
        return False


def update_credentials(new_username, new_password, username, platform):
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
                        "WHERE username = '{}' AND platform = '{}'").format(new_username, new_password, today, username,
                                                                            platform)

    connector = get_database_connector()
    cursor = connector.cursor()
    cursor.execute(update_query)
    connector.commit()
    connector.close()


def get_credentials(target_platform):
    connector = get_database_connector()
    cursor = connector.cursor()

    if target_platform == "all":
        get_all_credentials_query = "SELECT username, password, platform FROM credentials"
        cursor.execute(get_all_credentials_query)
    else:
        get_credentials_with_platform = "SELECT username, password, platform FROM credentials WHERE platform = '{}'".format(
            target_platform)
        cursor.execute(get_credentials_with_platform)

    credentials = []
    if any(cursor):
        for (username, password, platform) in cursor:
            credentials.append({'username': username, 'password': password, 'platform': platform})
    return credentials


def delete_credentials(username="all", platform="all"):
    if username == "all" and platform == "all":
        delete_query = "DELETE FROM credentials"
    else:
        delete_query = "DELETE FROM credentials " \
                       "WHERE username = '{}' AND platform = '{}'".format(username, platform)

    connector = get_database_connector()
    cursor = connector.cursor()
    cursor.execute(delete_query)
    connector.commit()
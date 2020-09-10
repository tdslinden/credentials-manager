import mysql.connector
import config


def main():
    print("~~~ Credentials Database ~~~")
    password = input("Enter password: ")
    check_master_password(password)


def check_master_password(password):
    correct_password = config.master_password
    while password != correct_password:
        password = input("Enter password: ")
    print(password)
    return True


if __name__ == '__main__':
    main()

cnx = mysql.connector.connect(user=config.root,
                              password=config.password,
                              host=config.host,
                              database=config.database)
if cnx.is_connected():
    db_info = cnx.get_server_info()
    print(db_info)

cnx.close()

#!/usr/bin/python3


from mysql.connector import connect, Error


def mysql_py():
    print("Соединение устанавливается")
    try:
        with connect(
                host="141.8.193.236",
                user="f0659051_apwasilenko",
                password="apwasilenko",
        ) as connection:
            print(connection)
            print("Соединение уставновлено")
    except Error as e:
        print(e)
        print("Соединение не уставновлено")


if __name__ == '__main__':
    mysql_py()

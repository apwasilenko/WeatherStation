#!/usr/bin/python3
import pymysql
from config import host, user, password, database


def mysql_py(col):
    print("Соединение устанавливается")
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=database,
            cursorclass = pymysql.cursors.DictCursor,
        )
        print("Соединение установлено")
        print('-' * 20, '#' * 20, '-' * 20)

        try:
            # cursor = connection.cursor()

            with connection.cursor() as cursor:
                selectqyery = ''

        finally:
            connection.close()
    except Exception as ex:
        print("Соединение не уставновлено")
        print(ex)


if __name__ == '__main__':
    mysql_py('10')

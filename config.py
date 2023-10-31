#!/usr/bin/python3
import pymysql
from mydataNoConnect import dateNoConnect


host = "141.8.193.236"
user ="f0659051_apwasilenko"
password="apwasilenko"
database="f0659051_apwasilenko"
myRezault = None


def mysql_py(col):

    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor,
        )
        try:
            with connection.cursor() as cursor:
                selectqyery = "SELECT * FROM temperatura ORDER BY temperatura.id DESC LIMIT " + str(col)
                cursor.execute(selectqyery)
                rows = cursor.fetchall()
                myRezault = rows
        finally:
            connection.close()
    except Exception as ex:
        print("Соединение не уставновлено")
        print(ex)
        myRezault = dateNoConnect
    print(myRezault)
    return myRezault


#!/usr/bin/python3


from mysql.connector import connect, Error


def mysql_py():
    try:
        with connect(
                host="141.8.193.236",
                user="f0659051_apwasilenko",
                password="apwasilenko",
        ) as connection:
            print(connection)
    except Error as e:
        print(e)

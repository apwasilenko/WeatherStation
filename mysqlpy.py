#!/usr/bin/python3


from mysql.connector import connect, Error


def mysql_py(col):
    print("Соединение устанавливается")
    try:
        with connect(
                host="141.8.193.236",
                user="f0659051_apwasilenko",
                password="apwasilenko",
                database="f0659051_apwasilenko",
        ) as connection:
            print(connection)
            print("Соединение уставновлено")
            select_movies_query = "SELECT * FROM temperatura ORDER BY temperatura.id DESC LIMIT " + col
            with connection.cursor() as cursor:
                cursor.execute(select_movies_query)
                result = cursor.fetchall()
                print(result)
                for row in result:
                    print(row)
    except Error as e:
        print(e)
        print("Соединение не уставновлено")


if __name__ == '__main__':
    mysql_py('10')

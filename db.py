import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    # password="root"
    database="mydatabase"
)
cursor = db.cursor()

# creates a database called client_server_app
"""cursor.execute("CREATE DATABASE client_server_app")"""

# creates a table called customers
"""cursor.execute("CREATE TABLE customers(username VARCHAR(255) PRIMARY KEY, password VARCHAR(255), name VARCHAR(
    255)," " surname VARCHAR(255), jmbg VARCHAR(13), email VARCHAR(255), tickets INT)") """


# inserts values into the table
def insert(val):
    sql = "INSERT INTO customers2(username, password, name, surname, jmbg, email) VALUES (%s, %s, %s, %s, %s, %s) "
    cursor.execute(sql, val)
    db.commit()
    print(cursor.rowcount, "was inserted.")


# selects values from the table
def select(sel):
    cursor.execute(f"SELECT {sel} FROM customers2")
    result = cursor.fetchall()
    for x in result:
        print(x)


def sumOfTickets():
    cursor.execute("SELECT SUM(tickets) from customers")
    print(cursor.fetchall()[0][0])

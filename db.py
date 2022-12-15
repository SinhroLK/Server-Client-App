import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    # password="root"
    database="mydatabase"
)
cursor = db.cursor()
# buffered = True - ako nesto ne radi, ovo ce da ga resi

# cursor.execute('SHOW DATABASE')

# creates a database called client_server_app
"""cursor.execute("CREATE DATABASE client_server_app")"""

# creates a table called customers
"""cursor.execute("CREATE TABLE server_client(username VARCHAR(255) PRIMARY KEY, password VARCHAR(255), name VARCHAR(255), "
               "surname VARCHAR(255), jmbg VARCHAR(13), email VARCHAR(255), tickets INT, vip_tickets INT)")"""


# inserts values into the table
def insert(val):
    sql = "INSERT INTO server_client(username, password, name, surname, jmbg, email, tickets, vip_tickets) VALUES (" \
          "%s, %s, %s, %s, %s, %s, %s, %s) "
    cursor.execute(sql, val)
    db.commit()
    print(cursor.rowcount, "was inserted.")


# selects values from the table
def select(sel):
    cursor.execute(f"SELECT {sel} FROM customers2")
    result = cursor.fetchall()
    results = []
    for x in result:
        results.append(x)
    return results


def sumOfTickets():
    cursor.execute("SELECT SUM(tickets) from server_client")
    print(cursor.fetchall()[0][0])


def sumOfVipTickets():
    cursor.execute("SELECT SUM(vip_tickets) from server_client")
    print(cursor.fetchall()[0][0])


def getReservation(tickets, username, numOfTickets):
    cursor.execute(f'UPDATE server_client SET {tickets} = {numOfTickets} WHERE username = {username}')
    db.commit()


def cancelReservation(tickets, username):
    cursor.execute(f'UPDATE server_client SET {tickets} = {0} WHERE username = {username}')
    db.commit()
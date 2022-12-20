import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    # password="root"
    database="client_server_app"
)
cursor = db.cursor(buffered=True)
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
    cursor.execute(f"SELECT {sel} FROM server_client")
    result = cursor.fetchall()
    #print(result)
    results = []
    for x in result:
        results.append(x)
    return results


def sumOfTickets():
    cursor.execute("SELECT SUM(tickets) from server_client")
    s = cursor.fetchall()[0][0]
    # print(s)
    return s


def sumOfVipTickets():
    cursor.execute("SELECT SUM(vip_tickets) from server_client")
    s = cursor.fetchall()[0][0]
    return s


def getNormalReservation(username, numOfTickets):
    cursor.execute('''UPDATE server_client SET tickets = %s WHERE username = %s''', (numOfTickets, username))
    db.commit()
    print(username, ' successfully bought ', str(numOfTickets), ' tickets')


def getVIPReservation(username, numOfTickets):
    cursor.execute('''UPDATE server_client SET vip_tickets = %s WHERE username = %s''', (numOfTickets, username))
    db.commit()
    print(username, ' successfully bought ', str(numOfTickets), ' tickets')


def cancelNormalReservation(username, userTics):
    userNormal, userVIP = userTickets(username)
    cursor.execute('''UPDATE server_client SET tickets = %s WHERE username = %s''', (userNormal - userTics, username,))
    db.commit()


def cancelVIPReservation(username, userTics):
    userNormal, userVIP = userTickets(username)
    cursor.execute('''UPDATE server_client SET vip_tickets = %s WHERE username = %s''', (userVIP - userTics, username))
    db.commit()


def userTickets(username):
    cursor.execute('SELECT tickets, vip_tickets FROM server_client WHERE username = %s', (username,))
    result = cursor.fetchall()[0]
    return result


def delete():
    sql = "DELETE FROM server_client where username = 'root5'"
    cursor.execute(sql)
    db.commit()
    print(cursor.rowcount, 'deleted')

import socket
import threading
from db import insert, select, sumOfTickets

FORMAT = 'utf-8'
HEADER = 1024
serverPort = 5055
serverName = socket.gethostbyname(socket.gethostname())
DISCONNECT_MSG = "!DISCONNECT"


def buyTickets():
    print('idk')


def logIn():
    username = connectionSocket.recv(HEADER).decode()
    password = connectionSocket.recv(HEADER).decode()
    tusername = (username,)
    tpassword = (password,)
    usernamesCheck = select('username')
    print(usernamesCheck)
    passwordsCheck = select('password')
    print(passwordsCheck)
    print(tusername in usernamesCheck and tpassword in passwordsCheck)
    print(usernamesCheck.index(tusername) == passwordsCheck.index(tpassword))
    print(usernamesCheck.index(tusername))
    print(passwordsCheck.index(tpassword))
    if tusername in usernamesCheck and tpassword in passwordsCheck:
        if usernamesCheck.index(tusername) == passwordsCheck.index(tpassword):
            return True
        else:
            return False


def signUp():
    username = connectionSocket.recv(HEADER).decode()
    password = connectionSocket.recv(HEADER).decode()
    name = connectionSocket.recv(HEADER).decode()
    surname = connectionSocket.recv(HEADER).decode()
    jmbg = connectionSocket.recv(HEADER).decode()
    email = connectionSocket.recv(HEADER).decode()
    insert((username, password, name, surname, jmbg, email))


def handleClient(connection, address):
    print(f'New connection at {address}')
    connection.send('Connection established'.encode())
    connected = True
    while connected:
        # connection.send('WAITING FOR A MESSAGE'.encode(FORMAT))
        msg = connection.recv(HEADER).decode()
        if msg == '1':
            if logIn():
                connection.send('SUCCESSFULLY LOGGED IN'.encode(FORMAT))
                thread_tickets = threading.Thread(target=buyTickets)
                thread_tickets.start()
        elif msg == '2':
            signUp()

    connection.close()


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(10)
print('Server is ready')
while True:
    connectionSocket, addr = serverSocket.accept()
    thread = threading.Thread(target=handleClient, args=(connectionSocket, addr))
    thread.start()
    print(f"Active Connections: {threading.active_count() - 1}")
# connectionSocket.close()

import socket
import threading

DISCONNECT_MSG = "!DISCONNECT"
FORMAT = 'utf-8'
HEADER = 1024



def logIn():
    username = input("Username: ")
    clientSocket.send(username.encode(FORMAT))
    password = input("Password: ")
    clientSocket.send(password.encode(FORMAT))
    print(clientSocket.recv(HEADER).decode(FORMAT))


def signUp():
    username = input("Username: ")
    password = input("Password: ")
    name = input("Name: ")
    surname = input("Surname: ")
    jmbg = input("JMBG: ")
    email = input("Email: ")
    if len(jmbg) == 13:
        clientSocket.send(username.encode(FORMAT))
        clientSocket.send(password.encode(FORMAT))
        clientSocket.send(name.encode(FORMAT))
        clientSocket.send(surname.encode(FORMAT))
        clientSocket.send(jmbg.encode(FORMAT))
        clientSocket.send(jmbg.encode(FORMAT))
    else:
        signUp()


serverPort = 5055
serverName = socket.gethostbyname(socket.gethostname())
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
connected = True
while connected:
    msg = clientSocket.recv(1024)
    print(msg.decode(FORMAT))
    print("1. Log in")
    print("2. Sign up")
    msg = input("Log in(1)/Sign up(2): ")
    clientSocket.send(msg.encode(FORMAT))
    if msg == '1':
        logIn()
    elif msg == '2':
        signUp()
    print(clientSocket.recv(HEADER).decode(FORMAT))
clientSocket.close()

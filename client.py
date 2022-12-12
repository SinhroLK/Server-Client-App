import socket
import threading

DISCONNECT_MSG = "!DISCONNECT"
FORMAT = 'utf-8'
HEADER = 1024

serverPort = 5052
serverName = socket.gethostbyname(socket.gethostname())
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
connected = True
while connected:
    msg = clientSocket.recv(1024)
    print(msg.decode(FORMAT))
    msg = input(">")
    clientSocket.send(msg.encode())
    if msg == DISCONNECT_MSG:
        connected = False
    else:
        msg = clientSocket.recv(1024)
        print(msg.decode())
clientSocket.close()

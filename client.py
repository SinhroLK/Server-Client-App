import socket
import threading

DISCONNECT_MSG = "!DISCONNECT"

serverName = 'localHost'
serverPort = 55001
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
connected = True
while connected:
    msg = input(">")
    clientSocket.send(msg.encode())
    if msg == DISCONNECT_MSG:
        connected = False
    else:
        msg = clientSocket.recv(1024)
        print(msg.decode())
clientSocket.close()

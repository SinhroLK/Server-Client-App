from socket import *
import mysql.connector
import threading
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('Server is ready')
while True:
    connectionSocket, addr = serverSocket.accept()
    connectionSocket.send('Connection established'.encode())
    connectionSocket.close()

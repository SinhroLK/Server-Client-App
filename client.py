from socket import *
serverName = 'localHost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
print(clientSocket.recv(1024).decode())

clientSocket.close()

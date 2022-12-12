import socket
import mysql.connector
import threading

DISCONNECT_MSG = "!DISCONNECT"


def handleClient(connection, address):
    print(f'New connection at {address}')
    connection.send('Connection established'.encode())
    connection.send('Type !DISCONNECT to disconnect from the server'.encode())
    connected = True
    while connected:
        msg = connection.recv(1024).decode()
        if msg == DISCONNECT_MSG:
            connected = False
        else:
            print(msg)
            connection.send('Msg received'.encode())
    connection.close()


serverPort = 55001
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('localHost', serverPort))
serverSocket.listen(10)
print('Server is ready')
while True:
    connectionSocket, addr = serverSocket.accept()
    thread = threading.Thread(target=handleClient, args=(connectionSocket, addr))
    thread.start()
    print(f"Active Connections: {threading.active_count() - 1}")
    connectionSocket.close()

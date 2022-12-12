import socket
import mysql.connector
import threading

FORMAT = 'utf-8'
HEADER = 1024
serverPort = 5052
serverName = socket.gethostbyname(socket.gethostname())
DISCONNECT_MSG = "!DISCONNECT"


def handleClient(connection, address):
    print(f'New connection at {address}')
    connection.send('Connection established'.encode())
    connected = True
    while connected:
        connection.send('WAITING FOR A MESSAGE'.encode(FORMAT))
        msg = connection.recv(HEADER).decode()
        if msg == DISCONNECT_MSG:
            connected = False
        print(msg)
        connection.send('MESSAGE RECEIVED'.encode(FORMAT))
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

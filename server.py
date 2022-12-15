import socket
import threading
from db import insert, select, sumOfTickets, sumOfVipTickets, getReservation, cancelReservation

FORMAT = 'utf-8'
HEADER = 1024
serverPort = 5057
serverName = socket.gethostbyname(socket.gethostname())
TOTAL_TICKETS = 20
TOTAL_VIP_TICKETS = 5


def buyTickets():
    connectionSocket.send('SUCCESSFULLY LOGGED IN'.encode(FORMAT))
    while True:
        currentSum = TOTAL_TICKETS - int(sumOfTickets())
        currentSumVip = TOTAL_VIP_TICKETS - int(sumOfVipTickets())
        connectionSocket.send(str(currentSum).encode(FORMAT))
        connectionSocket.send(str(currentSumVip).encode(FORMAT))
        flag = connectionSocket.recv(HEADER).decode(FORMAT)
        if flag == '1':
            """print('How many tickets would you like to buy?(max 4)')
            numOfTickets = 0
            while numOfTickets <= 0:
                numOfTickets = int(input())
                if numOfTickets <= 0 or numOfTickets > 4:
                    print("Number of tickets must be less than 4 and more than 0")
                    numOfTickets = 0
            if currentSum - numOfTickets < 0 or currentSum == 0:
                print('There are not enough tickets')"""
            numOfTickets = int(connectionSocket.recv(HEADER).decode(FORMAT))
            getReservation('tickets', username, numOfTickets)

        elif flag == '2':
            numOfTickets = int(connectionSocket.recv(HEADER).decode(FORMAT))
            getReservation('vip_tickets', username, numOfTickets)
        elif flag == '3':
            pass
        elif flag == '4':
            pass


def logIn():
    username = connectionSocket.recv(HEADER).decode()
    password = connectionSocket.recv(HEADER).decode()
    tusername = (username,)
    tpassword = (password,)
    usernamesCheck = select('username')
    passwordsCheck = select('password')
    if tusername in usernamesCheck and tpassword in passwordsCheck:
        if usernamesCheck.index(tusername) == passwordsCheck.index(tpassword):
            return True
        else:
            return False


def signUp():
    username = connectionSocket.recv(HEADER).decode()
    usernames = select(username)
    tusername = (username,)

    if tusername not in usernames:
        connectionSocket.send('Username available'.encode(FORMAT))
    else:
        connectionSocket.send('Username unavailable, choose other username'.encode(FORMAT))
        signUp()

    password = connectionSocket.recv(HEADER).decode()
    name = connectionSocket.recv(HEADER).decode()
    surname = connectionSocket.recv(HEADER).decode()
    jmbg = connectionSocket.recv(HEADER).decode()
    email = connectionSocket.recv(HEADER).decode()

    insert((username, password, name, surname, jmbg, email, 0, 0))


def handleClient(connection, address):
    print(f'New connection at {address}')
    connection.send('Connection established'.encode())
    connected = True
    while connected:
        # connection.send('WAITING FOR A MESSAGE'.encode(FORMAT))
        msg = connection.recv(HEADER).decode()
        if msg == '1':
            if logIn():
                thread_tickets = threading.Thread(target=buyTickets)
                thread_tickets.start()
            else:
                logIn()
        elif msg == '2':
            signUp()

    connection.close()


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(10)
print('Server is ready')
while True:
    connectionSocket, addr = serverSocket.accept()
    thread = threading.Thread(target=handleClient, args=(connectionSocket, addr))
    thread.start()
    print(f"Active Connections: {threading.active_count() - 1}")
# connectionSocket.close()

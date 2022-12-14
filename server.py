import socket
import threading
from db import insert, select, sumOfTickets, sumOfVipTickets

FORMAT = 'utf-8'
HEADER = 1024
serverPort = 5056
serverName = socket.gethostbyname(socket.gethostname())
TOTAL_TICKETS = 20
TOTAL_VIP_TICKETS = 5


def buyTickets():
    connectionSocket.send('SUCCESSFULLY LOGGED IN'.encode(FORMAT))
    currentSum = TOTAL_TICKETS - sumOfTickets()
    currentSumVip = TOTAL_VIP_TICKETS - sumOfVipTickets()
    print('1. Buy Normal Tickets')
    print('2. Buy VIP Tickets')
    print('3. Cancel reservation')
    print('4. Quit')
    flag = input('Choose one option: ')
    if flag == '1':
        print('How many tickets would you like to buy?(max 4)')
        numOfTickets = 0
        while numOfTickets <= 0:
            numOfTickets = int(input())
            if numOfTickets <= 0 or numOfTickets > 4:
                print("Number of tickets must be less than 4 and more than 0")
                numOfTickets = 0
        if currentSum - numOfTickets < 0 or currentSum == 0:
            print('There are not enough tickets')



    elif flag == '2':
        pass
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
                thread_tickets = threading.Thread(target=buyTickets)
                thread_tickets.start()
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

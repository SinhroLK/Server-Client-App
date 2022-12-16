import socket
import threading
from db import insert, select, sumOfTickets, sumOfVipTickets, getNormalReservation,getVIPReservation, \
    cancelNormalReservation, cancelVIPReservation, userTickets

FORMAT = 'utf-8'
HEADER = 1024
serverPort = 5057
serverName = socket.gethostbyname(socket.gethostname())
TOTAL_TICKETS = 20
TOTAL_VIP_TICKETS = 5


def buyTickets(username):
    connectionSocket.send('SUCCESSFULLY LOGGED IN'.encode(FORMAT))
    #print(connectionSocket.recv(HEADER).decode(FORMAT))
    while True:
        print(int(sumOfTickets()))
        currentSum = TOTAL_TICKETS - sumOfTickets()
        currentSumVip = TOTAL_VIP_TICKETS - int(sumOfVipTickets())
        print(currentSum, currentSumVip)
        connectionSocket.send((str(currentSum)).encode(FORMAT))
        connectionSocket.send((str(currentSumVip)).encode(FORMAT))
        flag = connectionSocket.recv(HEADER).decode(FORMAT)
        if flag == '1':
            numOfTickets = int(connectionSocket.recv(HEADER).decode(FORMAT))
            print(numOfTickets)
            getNormalReservation(username, numOfTickets)

        elif flag == '2':
            numOfTickets = int(connectionSocket.recv(HEADER).decode(FORMAT))
            getVIPReservation(username, numOfTickets)
        elif flag == '3':
            pass
        elif flag == '4':
            pass


def logIn(username, password):
    tusername = (username,)
    tpassword = (password,)
    usernamesCheck = select('username')
    passwordsCheck = select('password')
    if tusername in usernamesCheck and tpassword in passwordsCheck:
        if usernamesCheck.index(tusername) == passwordsCheck.index(tpassword):
            connectionSocket.send('1'.encode(FORMAT))
            return True
        else:
            connectionSocket.send('Incorrect username or password'.encode(FORMAT))
            return False


def signUp():
    username = connectionSocket.recv(HEADER).decode()
    usernames = select('username')
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
    return username


def handleClient(connection, address):
    print(f'New connection at {address}')
    connection.send('Connection established'.encode())
    connected = True
    while connected:
        # connection.send('WAITING FOR A MESSAGE'.encode(FORMAT))
        msg = connection.recv(HEADER).decode()
        if msg == '1':
            username = connectionSocket.recv(HEADER).decode()
            password = connectionSocket.recv(HEADER).decode()
            if logIn(username, password):
                thread_tickets = threading.Thread(target=buyTickets, args=(username,))
                thread_tickets.start()
            else:
                logIn(username, password)
        elif msg == '2':
            username = signUp()
            thread_tickets = threading.Thread(target=buyTickets, args=(username,))
            thread_tickets.start()

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

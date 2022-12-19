import socket
import threading
from db import insert, select, sumOfTickets, sumOfVipTickets, getNormalReservation, getVIPReservation, \
    cancelNormalReservation, cancelVIPReservation, userTickets

FORMAT = 'utf-8'
HEADER = 1024
serverPort = 5051
serverName = socket.gethostbyname(socket.gethostname())
TOTAL_TICKETS = 20
TOTAL_VIP_TICKETS = 5


def buyTicketsServer(username):
    # connectionSocket.send('SUCCESSFULLY LOGGED IN'.encode(FORMAT))
    # print(connectionSocket.recv(HEADER).decode(FORMAT))
    while True:
        # calculates current number of availble tickets of both kinds
        currentSum = TOTAL_TICKETS - sumOfTickets()
        currentSumVip = TOTAL_VIP_TICKETS - int(sumOfVipTickets())
        # sends the respective amounts to the client
        connectionSocket.send((str(currentSum)).encode(FORMAT))
        connectionSocket.send((str(currentSumVip)).encode(FORMAT))
        # receives the flag from the client
        flag = connectionSocket.recv(HEADER).decode(FORMAT)
        # gets the number of tickets the user already has, normal and vip respectively
        numOfTicketsNormal, numOfTicketsVIP = userTickets(username)
        # sums the total amount of tickets the user has
        numOfTickets = numOfTicketsNormal + numOfTicketsVIP
        if flag == '1':
            # sends the current amount of tickets the clients has to the client
            connectionSocket.send((str(numOfTickets)).encode(FORMAT))
            # receives how many tickets the client wants to buy
            msg = connectionSocket.recv(HEADER).decode(FORMAT)
            # checks whether user wants the amount he can get
            if msg == 'sum more than 4' or msg == 'not enough tickets':
                buyTicketsServer(username)
            else:
                numOfTickets = int(connectionSocket.recv(HEADER).decode(FORMAT))
                getNormalReservation(username, numOfTickets)
            buyTicketsServer(username)

        elif flag == '2':
            connectionSocket.send((str(numOfTickets)).encode(FORMAT))
            numOfTickets = int(connectionSocket.recv(HEADER).decode(FORMAT))
            getVIPReservation(username, numOfTickets)
            buyTicketsServer(username)
        elif flag == '3':
            userNormal, userVIP = userTickets(username)
            connectionSocket.send((str(userNormal)).encode(FORMAT))
            connectionSocket.send((str(userVIP)).encode(FORMAT))
            msg = connectionSocket.recv(HEADER).decode(FORMAT)
            userTics = int(connectionSocket.recv(HEADER).decode(FORMAT))
            if msg == '1':
                cancelNormalReservation(username, userTics)
            elif msg == '2':
                cancelVIPReservation(username, userTics)
            connectionSocket.send('You have successfully canceled your reservations'.encode(FORMAT))
            buyTicketsServer(username)
        elif flag == '4':
            availableNormal = TOTAL_TICKETS - sumOfTickets()
            availableVip = TOTAL_VIP_TICKETS - sumOfVipTickets()
            connectionSocket.send((str(availableNormal)).encode(FORMAT))
            connectionSocket.send((str(availableVip)).encode(FORMAT))
            buyTicketsServer(username)
        else:
            print(username, ' disconnected')


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
                """thread_tickets = threading.Thread(target=buyTickets, args=(username,))
                thread_tickets.start()"""
            else:
                logIn(username, password)
        elif msg == '2':
            username = signUp()
            # print(username)
        else:
            handleClient(connection, address)
        connectionSocket.send('SUCCESSFULLY LOGGED IN'.encode(FORMAT))
        # thread_tickets_server = threading.Thread(target=buyTicketsServer, args=(username,))
        # thread_tickets_server.start()
        buyTicketsServer(username)

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

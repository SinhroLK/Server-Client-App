import socket
import threading

FORMAT = 'utf-8'
HEADER = 1024
TOTAL_TICKETS = 20
TOTAL_VIP_TICKETS = 5
username = ''


def buyTickets():
    print(clientSocket.recv(HEADER).decode(FORMAT))
    while True:
        currentSum = int(clientSocket.recv(HEADER).decode(FORMAT))
        currentSumVip = int(clientSocket.recv(HEADER).decode(FORMAT))

        print('1. Buy Normal Tickets')
        print('2. Buy VIP Tickets')
        print('3. Cancel reservation')
        print('4. Quit')
        flag = input('Choose one option: ')
        clientSocket.send(flag.encode(FORMAT))
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
                buyTickets()
            clientSocket.send(str(numOfTickets).encode(FORMAT))

        elif flag == '2':
            numOfTickets = 0
            while numOfTickets <= 0:
                numOfTickets = int(input())
                if numOfTickets <= 0:
                    print('Number of tickets has to be more than 0')
            if currentSumVip - numOfTickets < 0 or currentSumVip == 0:
                print('There are not enough tickets')
                buyTickets()
            clientSocket.send(str(numOfTickets).encode(FORMAT))
        elif flag == '3':
            print("You have disconnected.")
            clientSocket.close()
        elif flag == '4':
            pass


def logIn():
    global username
    username = input("Username: ")
    clientSocket.send(username.encode(FORMAT))
    password = input("Password: ")
    clientSocket.send(password.encode(FORMAT))


def signUp():
    global username
    username = input("Username: ")
    clientSocket.send(username.encode(FORMAT))
    if clientSocket.recv(HEADER).decode(FORMAT) == 'Username unavailable, choose other username':
        signUp()
    else:
        password = input("Password: ")
        clientSocket.send(password.encode(FORMAT))
        name = input("Name: ")
        clientSocket.send(name.encode(FORMAT))
        surname = input("Surname: ")
        clientSocket.send(surname.encode(FORMAT))
        jmbg = input("JMBG: ")
        if len(jmbg) == 13:
            clientSocket.send(jmbg.encode(FORMAT))
        else:
            print('JMBG has to be 13 characters long')
            signUp()
        email = input("Email: ")
        clientSocket.send(email.encode(FORMAT))


def receive():
    connected = True
    while connected:
        msg = clientSocket.recv(1024)
        print(msg.decode(FORMAT))
        print("1. Log in")
        print("2. Sign up")
        msg = input("Log in(1)/Sign up(2): ")
        clientSocket.send(msg.encode(FORMAT))
        if msg == '1':
            logIn()
            break
        elif msg == '2':
            signUp()
            break
        else:
            print('Please use correct input')
    thread_tickets = threading.Thread(target=buyTickets)
    thread_tickets.start()


serverPort = 5057
serverName = socket.gethostbyname(socket.gethostname())
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
thread_client = threading.Thread(target=receive)
thread_client.start()
# clientSocket.close()

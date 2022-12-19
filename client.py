import socket
import threading

FORMAT = 'utf-8'
HEADER = 1024
TOTAL_TICKETS = 20
TOTAL_VIP_TICKETS = 5
serverPort = 5051
serverName = socket.gethostbyname(socket.gethostname())
username = ''


def buyTickets():
    #print(clientSocket.recv(HEADER).decode(FORMAT))
    while True:
        currentAvailable = int(clientSocket.recv(HEADER).decode(FORMAT))
        currentAvailableVip = int(clientSocket.recv(HEADER).decode(FORMAT))

        print('1. Buy Normal Tickets')
        print('2. Buy VIP Tickets')
        print('3. Cancel reservation')
        print('4. Number of tickets available')
        print('5. Quit')
        flag = input('Choose one option: ')
        clientSocket.send(flag.encode(FORMAT))
        if flag == '1':
            print('How many tickets would you like to buy?(max 4)')
            newTickets = 0  # num of tickets client wants to buy
            currTickets = int(clientSocket.recv(HEADER).decode(FORMAT))  # curr amount the client has
            while newTickets <= 0:  # inputs the amount the client wants until it's a number we can work with
                newTickets = int(input())
                if newTickets <= 0 or newTickets > 4:
                    print("Number of tickets must be less than 4 and more than 0, pick another number:")
                    newTickets = 0
            if currTickets + newTickets > 4:  # checks if client has more than 4 tickets with the new ones
                print("You can't have more than 4 tickets")
                clientSocket.send('sum more than 4'.encode(FORMAT))
                buyTickets()

            if currentAvailable - newTickets < 0 or currentAvailable == 0:  # checks if there are enough tickets to buy
                print('There are not enough tickets')
                clientSocket.send('not enough tickets'.encode(FORMAT))
                buyTickets()

            clientSocket.send((str(newTickets)).encode(FORMAT))
            clientSocket.send((str(newTickets)).encode(FORMAT))
            buyTickets()

        elif flag == '2':
            print('How many tickets would you like to buy?(max 4)')
            newTickets = 0
            currTickets = int(clientSocket.recv(HEADER).decode(FORMAT))
            while newTickets <= 0:
                newTickets = int(input())
                if newTickets <= 0:
                    print('Number of tickets has to be more than 0, choose other number')
            if currTickets + newTickets > 4:
                print("You can't have more than 4 tickets")
                clientSocket.send('sum more than 4'.encode(FORMAT))
                buyTickets()
            if currentAvailableVip - newTickets < 0 or currentAvailableVip == 0:
                print('There are not enough tickets')
                buyTickets()
            clientSocket.send(str(newTickets).encode(FORMAT))
        elif flag == '3':
            userNormal = int(clientSocket.recv(HEADER).decode(FORMAT))
            userVIP = int(clientSocket.recv(HEADER).decode(FORMAT))
            print('1. Cancel normal reservations')
            print('2. Cancel VIP reservations')
            print('3. Back to menu')
            msg = ''
            num = 0
            while msg != '1' and msg != '2':
                msg = input('Input your choice: ')
                clientSocket.send(msg.encode(FORMAT))
                if msg == '1':
                    while num > userNormal or num == 0:
                        num = int(input('How many reservations would you like to cancel(less than or equal to the number you have): '))
                elif msg == '2':
                    while num > userVIP or num == 0:
                        num = int(input('How many reservations would you like to cancel(less than or equal to the number you have): '))
                elif msg == '3':
                    buyTickets()
                else:
                    print('Please use correct input')
            clientSocket.send((str(num)).encode(FORMAT))
            #clientSocket.send(username.encode(FORMAT))
            print(clientSocket.recv(HEADER).decode(FORMAT))
            buyTickets()
        elif flag == '4':
            print('Currently available normal tickets: ', clientSocket.recv(HEADER).decode(FORMAT))
            print('Currently available VIP tickets', clientSocket.recv(HEADER).decode(FORMAT))
            buyTickets()
        elif flag == '5':
            print("You have disconnected.")
            clientSocket.close()
        buyTickets()


def logIn():
    global username
    username = input("Username: ")
    clientSocket.send(username.encode(FORMAT))
    password = input("Password: ")
    clientSocket.send(password.encode(FORMAT))
    msg = clientSocket.recv(HEADER).decode(FORMAT)
    if msg == 'Incorrect username or password':
        print(msg)
        logIn()


def signUp():
    global username
    username = input("Username: ")
    clientSocket.send(username.encode(FORMAT))
    msg = clientSocket.recv(HEADER).decode(FORMAT)
    print(msg)
    if msg == 'Username unavailable, choose other username':
        clientSocket.close()
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
    msg = clientSocket.recv(1024)
    print(msg.decode(FORMAT))
    while connected:

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
            receive()
    # buyTickets()
    print('\n', clientSocket.recv(HEADER).decode(FORMAT))
    thread_tickets_client = threading.Thread(target=buyTickets)
    thread_tickets_client.start()


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
thread_client = threading.Thread(target=receive)
thread_client.start()
# clientSocket.close()

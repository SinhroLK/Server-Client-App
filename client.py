import threading
import socket

FORMAT = 'utf-8'
HEADER = 1024
TOTAL_TICKETS = 20
TOTAL_VIP_TICKETS = 5
serverPort = 5051
serverName = socket.gethostbyname(socket.gethostname())
username = ''
stop = False
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))


def registration():
    while True:
        global username
        global stop
        if stop:
            break
        try:
            print("1. Log in")
            print("2. Sign up")
            msg = input("Log in(1)/Sign up(2): ")
            clientSocket.send(msg.encode(FORMAT))
            if msg == '1':
                username = input('Username: ')
                clientSocket.send(username.encode(FORMAT))
                password = input('Password: ')
                clientSocket.send(password.encode(FORMAT))
                msg = clientSocket.recv(HEADER).decode(FORMAT)
                if msg == 'ACCESS DENIED':
                    print('Wrong username or password')
                    stop = True
            elif msg == '2':
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
                    while len(jmbg) != 13:
                        print('JMBG has to be 13 characters long')
                        jmbg = input("JMBG: ")
                    clientSocket.send(jmbg.encode(FORMAT))
                    email = input("Email: ")
                    clientSocket.send(email.encode(FORMAT))
            else:
                print('Please use correct input')
            break
        except:
            print('Client uginuo')
            clientSocket.close()
            break
    try:
        print(clientSocket.recv(HEADER).decode(FORMAT))
        thread_ticekting = threading.Thread(target=ticketing, args=(username,))
        thread_ticekting.start()
    except:
        print('Client closed')


def ticketing(username):
    global stop
    if not stop:
        print('Thank you for using our ticketing system')
    while True:
        if stop:
            break
        try:
            while True:
                print('1. Buy Normal Tickets')
                print('2. Buy VIP Tickets')
                print('3. Cancel reservation')
                print('4. Number of tickets available')
                print('5. Quit')
                msg = input('Choose one option: ')
                if msg not in ['1', '2', '3', '4', '5']:
                    print('Choose correct input')
                    break
                clientSocket.send(msg.encode(FORMAT))
                if msg == '1':
                    print('How many tickets would you like to buy(max 4)?')
                    newTickets = int(input())
                    while newTickets < 0 or newTickets > 4:
                        print('You can only buy more than 0 and less than 4 ticekts, try again')
                        newTickets = int(input())
                    clientSocket.send((str(newTickets)).encode(FORMAT))
                    print(clientSocket.recv(HEADER).decode(FORMAT))
                elif msg == '2':
                    print('How many tickets would you like to buy(max 4)?')
                    newTickets = int(input())
                    while newTickets < 0 or newTickets > 4:
                        print('You can only buy more than 0 and less than 4 ticekts, try again')
                        newTickets = int(input())
                    clientSocket.send((str(newTickets)).encode(FORMAT))
                    print(clientSocket.recv(HEADER).decode(FORMAT))
                elif msg == '3':
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
                        print(clientSocket.recv(HEADER).decode(FORMAT))
                        if msg == '1':
                            while num > userNormal or num == 0:
                                num = int(input(
                                    'How many reservations would you like to cancel(less than or equal to the number you have): '))
                        elif msg == '2':
                            while num > userVIP or num == 0:
                                num = int(input(
                                    'How many reservations would you like to cancel(less than or equal to the number you have): '))
                        elif msg == '3':
                            break
                        else:
                            print('Please use correct input')
                    clientSocket.send((str(num)).encode(FORMAT))
                    # clientSocket.send(username.encode(FORMAT))
                    print(clientSocket.recv(HEADER).decode(FORMAT))
                elif msg == '4':
                    print('Currently available normal tickets: ', clientSocket.recv(HEADER).decode(FORMAT))
                    print('Currently available VIP tickets', clientSocket.recv(HEADER).decode(FORMAT))
                elif msg == '5':
                    print('Hope to see you again soon')
                    stop = True
                    break
        except:
            print('You left')


if __name__ == "__main__":
    try:
        receive_thread = threading.Thread(target=registration)
        receive_thread.start()
    except:
        print("Client closed")

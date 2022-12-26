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
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((serverName, serverPort))
serverSocket.listen()


def tickets(connection, username):
    while True:
        try:
            # calculates current number of availble tickets of both kinds
            currentSum = TOTAL_TICKETS - int(sumOfTickets())
            currentSumVip = TOTAL_VIP_TICKETS - int(sumOfVipTickets())
            numOfTicketsNormal, numOfTicketsVIP = userTickets(username)
            numOfTickets = numOfTicketsNormal + numOfTicketsVIP
            userNormal, userVip = userTickets(username)
            msg = connection.recv(HEADER).decode(FORMAT)
            if msg == '1':
                newTickets = int(connection.recv(HEADER).decode(FORMAT))
                print(newTickets)
                if currentSum <= 0 or currentSum - newTickets < 0 or numOfTickets + newTickets > 4:
                    connection.send('There are not enough tickets or you have already bought 4'.encode(FORMAT))
                else:
                    getNormalReservation(username, newTickets)
                    connection.send(f'You have successfully bought {newTickets} tickets'.encode(FORMAT))
            elif msg == '2':
                newTickets = int(connection.recv(HEADER).decode(FORMAT))
                print(newTickets)
                if currentSumVip <= 0 or currentSumVip - newTickets < 0 or numOfTickets + newTickets > 4:
                    connection.send('There are not enough tickets or you have already bought 4'.encode(FORMAT))
                else:
                    getVIPReservation(username, newTickets)
                    connection.send(f'You have successfully bought {newTickets} tickets'.encode(FORMAT))
            elif msg == '3':
                connection.send((str(userNormal)).encode(FORMAT))
                connection.send((str(userVip)).encode(FORMAT))
                msg = connection.recv(HEADER).decode(FORMAT)
                connection.send(f'You have {userNormal} normal tickets and {userVip} VIP tickets'.encode(FORMAT))
                userTics = int(connection.recv(HEADER).decode(FORMAT))
                if msg == '1':
                    cancelNormalReservation(username, userTics)
                elif msg == '2':
                    cancelVIPReservation(username, userTics)
                connection.send('You have successfully canceled your reservations'.encode(FORMAT))
            elif msg == '4':
                availableNormal = TOTAL_TICKETS - sumOfTickets()
                availableVip = TOTAL_VIP_TICKETS - sumOfVipTickets()
                connection.send((str(availableNormal)).encode(FORMAT))
                connection.send((str(availableVip)).encode(FORMAT))
            elif msg == '5':
                print(f'{username} left')
                break
        except:
            print('Connection with client ended')
            break


def handleClient(connection, addr):
    print(f'New connection at {addr}')
    try:
        msg = connection.recv(HEADER).decode(FORMAT)
        if msg == '1':
            username = connection.recv(HEADER).decode(FORMAT)
            password = connection.recv(HEADER).decode(FORMAT)
            tusername = (username,)
            tpassword = (password,)
            usernamesCheck = select('username')
            passwordsCheck = select('password')
            if tusername in usernamesCheck and tpassword in passwordsCheck:
                if usernamesCheck.index(tusername) == passwordsCheck.index(tpassword):
                    connection.send('ACCESS GRANTED'.encode(FORMAT))
                else:
                    connection.send('ACCESS DENIED'.encode(FORMAT))
                    print('Client left')
            else:
                connection.send('ACCESS DENIED'.encode(FORMAT))
                print('Client left')
        elif msg == '2':
            username = connection.recv(HEADER).decode()
            usernames = select('username')
            tusername = (username,)

            if tusername not in usernames:
                connection.send('Username available'.encode(FORMAT))
            else:
                connection.send('Username unavailable, choose other username'.encode(FORMAT))

            password = connection.recv(HEADER).decode()
            name = connection.recv(HEADER).decode()
            surname = connection.recv(HEADER).decode()
            jmbg = connection.recv(HEADER).decode()
            email = connection.recv(HEADER).decode()
            insert((username, password, name, surname, jmbg, email, 0, 0))
        connection.send('Connection established'.encode(FORMAT))
        thread_tickets = threading.Thread(target=tickets, args=(connection, username,))
        thread_tickets.start()
    except:
        print('Client removed by force')


if __name__ == "__main__":
    print('Server is ready')
    while True:
        connectionSocket, address = serverSocket.accept()
        thread_main = threading.Thread(target=handleClient, args=(connectionSocket, address,))
        thread_main.start()

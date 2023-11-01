import socket
import threading
import datetime

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
IP = socket.gethostbyname(socket.gethostname())
print(IP)
server.bind((IP,55555))
server.listen()

clients = []
nicknames = []

currentUserData = {}


def connectionWorks(clientConnection):
    # active users:
    print(f"Active users: {nicknames}")

    # who joined chat:
    for client in clients:
        if client != clientConnection:
            client.send(f"{currentUserData[clientConnection]} {id(clientConnection)} joined chat !".encode('utf8'))
    
    # receiving message and sending it to all clients:
    while True: 
        try:
            messageIn = clientConnection.recv(1024).decode('utf8')
            if not messageIn:
                clientConnection.close()
                break

            for client in clients:
                # send to everyone except user that is sending message:
                if client != clientConnection:
                    client.send(f"{currentUserData[clientConnection]} {id(clientConnection)}: {messageIn}".encode('utf8'))

        except ConnectionResetError:
            clientConnection.close()
            clients.remove(clientConnection)
            print(f"{datetime.datetime.now()} {currentUserData[clientConnection]} left the chat!")

            for client in clients:
                client.send(f"{currentUserData[clientConnection]} left the chat !".encode('utf8'))
            nicknames.remove(currentUserData[clientConnection])
            break
        

def receiveConnection(server):
    while True:
        
        clientConnection, addressIP = server.accept()
        nickOfUser = clientConnection.recv(1024).decode('utf8')
        print(f"{datetime.datetime.now()} {nickOfUser} joined chat!")

        nicknames.append(nickOfUser)
        clients.append(clientConnection)

        currentUserData[clientConnection] = nickOfUser

        newChat = threading.Thread(target = connectionWorks, args = (clientConnection,))
        newChat.start()
        

print(f"{datetime.datetime.now()} Hello ! server starts runnin..")
receiveThread = threading.Thread(target = receiveConnection,args=(server,))
receiveThread.start()
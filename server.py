import socket
import threading

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
IP = socket.gethostbyname(socket.gethostname())
print(IP)
server.bind((IP,55555))
server.listen()

clients = []
nicknames = []

currentUserData = {}


def connectionWorks(clientConnection):
    
    while True: 
        try:
            messageIn = clientConnection.recv(1024).decode('utf8')
            if not messageIn:
                clientConnection.close()
                break

            for client in clients:
                client.send(f"{currentUserData[clientConnection]}: {messageIn}".encode('utf8'))
        except ConnectionResetError:
            clientConnection.close()
            clients.remove(clientConnection)
            break
        #trzeba usunac z tabeli polaczenie z klientem zeby nie probowal po rozlaczeniu do niego wysylas wiadomosci

def receiveConnection(server):
    while True:
        
        clientConnection, addressIP = server.accept()
        nickOfUser = clientConnection.recv(1024).decode('utf8')

        nicknames.append(nickOfUser)
        clients.append(clientConnection)

        currentUserData[clientConnection] = nickOfUser

        newChat = threading.Thread(target = connectionWorks, args = (clientConnection,))
        newChat.start()
        

print("Hello ! server starts runnin..")
receiveThread = threading.Thread(target = receiveConnection,args=(server,))
receiveThread.start()
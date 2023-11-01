import socket
import threading

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
IP = socket.gethostbyname(socket.gethostname())
print(IP)
server.bind((IP,55555))
server.listen()

clients = []

def connectionWorks(clientConnection):
    
    while True: 
        messageIn = clientConnection.recv(1024).decode('utf8')
        print(messageIn)
        for client in clients:
            client.send(messageIn.encode('utf8'))

def receiveConnection(server):
    while True:
        
        clientConnection, addressIP = server.accept()
        

        newChat = threading.Thread(target = connectionWorks, args = (clientConnection,))
        newChat.start()
        clients.append(clientConnection)
        print(clients)


print("Hello ! server starts runnin..")
receiveThread = threading.Thread(target = receiveConnection,args=(server,))
receiveThread.start()
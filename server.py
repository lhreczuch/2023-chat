# for now it has to be in the same local connection as client

import socket
import threading
import datetime

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
IP = socket.gethostbyname(socket.gethostname())
print(IP)
server.bind((IP,55555))
server.listen()

connectedClients = {}

def connectionWorks(clientConnection):
    # active users:
    print(f"Active users: {connectedClients.values()}")

    # who joined chat:
    
    currentValue = connectedClients[clientConnection]
    currentKey = clientConnection
    # receiving message and sending it to all clients:
    while True: 
        try:
            messageIn = clientConnection.recv(1024).decode('utf8')

            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

            for client in connectedClients.keys():
                # send to everyone except user that is sending message:
                if client != currentKey:
                    client.send(f"[{formatted_time}] [{currentValue}]: {messageIn}".encode('utf8'))
                # send message also to sender, but with "ME"
                if client == currentKey:
                    client.send(f"[{formatted_time}] [ME]: {messageIn}".encode('utf8'))

        except ConnectionResetError:
            clientConnection.close()
            
            print(f"{datetime.datetime.now()} {currentValue} left the chat!")
            
            

            for client in connectedClients.keys():
                try:
                    client.send(f"{currentValue} left the chat !".encode('utf8'))
                except OSError:
                    continue
            
            del connectedClients[currentKey]
            break
    print(f"Active users: {connectedClients.values()}")

        
def receiveConnection(server):
    while True:
        clientConnection, addressIP = server.accept()
       
        nickOfUser = clientConnection.recv(1024).decode('utf8')
        
        print(f"{datetime.datetime.now()} {nickOfUser} joined chat!")

        connectedClients[clientConnection] = nickOfUser
        
        for client in connectedClients.keys():
            client.send(f"{datetime.datetime.now()} {nickOfUser} joined chat!".encode('utf8'))
            
        newChat = threading.Thread(target = connectionWorks, args = (clientConnection,))
        newChat.start()
        

print(f"{datetime.datetime.now()} Hello ! server starts runnin..")
receiveThread = threading.Thread(target = receiveConnection,args=(server,))
receiveThread.start()

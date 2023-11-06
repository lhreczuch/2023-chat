# for now it has to be in the same local connection as client

import socket
import threading
import datetime

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
IP = socket.gethostbyname(socket.gethostname())
print(IP)
server.bind((IP,55555))
server.listen()

connected_clients = {}

def connectionWorks(client_connection):
    # active users:
    print(f"Active users: {connected_clients.values()}")

    # who joined chat:
    
    current_value = connected_clients[client_connection]
    current_key = client_connection
    # receiving message and sending it to all clients:
    while True: 
        try:
            message_in = client_connection.recv(1024).decode('utf8')

            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

            for client in connected_clients.keys():
                # send to everyone except user that is sending message:
                if client != current_key:
                    client.send(f"[{formatted_time}] [{current_value}]: {message_in}".encode('utf8'))
                # send message also to sender, but with "ME"
                if client == current_key:
                    client.send(f"[{formatted_time}] [ME]: {message_in}".encode('utf8'))

        except ConnectionResetError:
            client_connection.close()
            
            print(f"{datetime.datetime.now()} {current_value} left the chat!")
            
            

            for client in connected_clients.keys():
                try:
                    client.send(f"{current_value} left the chat !".encode('utf8'))
                except OSError:
                    continue
            
            del connected_clients[current_key]
            break
    print(f"Active users: {connected_clients.values()}")

        
def receiveConnection(server):
    while True:
        client_connection, address_IP = server.accept()
       
        nick_of_user = client_connection.recv(1024).decode('utf8')
        
        print(f"{datetime.datetime.now()} {nick_of_user} joined chat!")

        connected_clients[client_connection] = nick_of_user
        
        for client in connected_clients.keys():
            client.send(f"{datetime.datetime.now()} {nick_of_user} joined chat!".encode('utf8'))
            
        new_chat = threading.Thread(target = connectionWorks, args = (client_connection,))
        new_chat.start()
        

print(f"{datetime.datetime.now()} Hello ! server starts runnin..")
receive_thread = threading.Thread(target = receiveConnection,args=(server,))
receive_thread.start()

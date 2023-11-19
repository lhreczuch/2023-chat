# for now it has to be in the same local connection as client

import socket
import threading
import datetime
import sqlite3

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

            if message_in.startswith("[DB]"):
                message_in = message_in[4:]
                db = sqlite3.connect('chat.db')
                cursor = db.cursor()
                cursor.execute(message_in)
                query_out = cursor.fetchall()
                db_message_back = ''
                for row in query_out:
                    db_message_back += ": ".join(map(str,row))+'\n'
                current_key.send(f"[DB] said:\n{db_message_back}".encode('utf8'))
                # db.commit()
                db.close()

            else:
                # disconnecting user row id from his nick:
                row_id = ""
                for i in current_value:
                    if i.isdigit():
                        row_id = row_id + i
                        continue
                    else:
                        break

                # adding received message to database with assigned user row id:
                db = sqlite3.connect('chat.db')
                cursor = db.cursor()
                cursor.execute("INSERT INTO messages VALUES (?,?,?)", (row_id,message_in,formatted_time))
                db.commit()
                db.close()

                current_time = datetime.datetime.now()
                formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

                for client in connected_clients.keys():
                    # send to everyone except user that is sending message:
                    if client != current_key:
                        client.send(f"[NDB{formatted_time}] [{current_value}]: {message_in}".encode('utf8'))
                    # send message also to sender, but with "ME"
                    if client == current_key:
                        client.send(f"[NDB{formatted_time}] [ME]: {message_in}".encode('utf8'))

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
        print(nick_of_user)

        # adding user to database when he connects
        db = sqlite3.connect('chat.db')
        cursor = db.cursor()
        cursor.execute("INSERT INTO users VALUES (?)",[nick_of_user])

        # fetching last user_id that was added to database - it is always going to be new user_id added to database above:
        cursor.execute("SELECT rowid FROM users ORDER BY rowid DESC LIMIT 1")
        wynik = cursor.fetchone()
        # if wynik:
        current_client_row_id = str(wynik[0])
        db.commit()
        db.close()
       
        
        print(f"{datetime.datetime.now()} {nick_of_user} joined chat!")

        # adding new item to clients dictionary. Value is a string of user_id and nick, so we can recognize current user afterwards:
        connected_clients[client_connection] = f"{current_client_row_id + nick_of_user}"
        
        for client in connected_clients.keys():
            client.send(f"[NDB{datetime.datetime.now()} {nick_of_user} joined chat!".encode('utf8'))
        
        
        new_chat = threading.Thread(target = connectionWorks, args = (client_connection,))
        new_chat.start()
        

print(f"{datetime.datetime.now()} Hello ! server starts runnin..")
receive_thread = threading.Thread(target = receiveConnection,args=(server,))
receive_thread.start()

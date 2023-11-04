import socket
import threading
nick = input("Wprowadź swój nick: ")

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('192.168.55.111',55555))


def send():
    
    while True:
        try:
            messageOut = f"{nick}: {input('')}"
            client.send(messageOut.encode('utf8'))

        except ConnectionAbortedError and ConnectionResetError:
            print("stracono połączenie z serwerem!")
            client.close()
            break


def receive():
    while True:
        try:
            messageIn = client.recv(1024).decode('utf8')
            if messageIn == "NICK":
                client.send(nick.encode('utf8'))
            else:
                print(messageIn)
                
        except ConnectionAbortedError and ConnectionResetError:
            print("stracono połączenie z serwerem!")
            client.close()
            break

receiveThread = threading.Thread(target = receive)        
receiveThread.start()  
sendThread = threading.Thread(target = send)
sendThread.start()

  




# na kliencie ktory zostal otwarty jako drugi nie chce sie wyslac nick, dopoki ten pierwszy nie wysle nicku...


import socket
import threading


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('192.168.55.111',55555))


def send():
    while True:
        try:
            messageOut = input('')
            client.send(messageOut.encode('utf8'))
        except ConnectionAbortedError and ConnectionResetError:
            print("stracono połączenie z serwerem!")
            break


def receive():
    while True:
        try:
            messageIn = client.recv(1024).decode('utf8')
            print(messageIn)
        except ConnectionAbortedError and ConnectionResetError:
            print("stracono połączenie z serwerem!")
            break
            
            
            

nick = input("Wprowadź swój nick: ")
client.send(nick.encode('utf8'))

sendThread = threading.Thread(target = send)
receiveThread = threading.Thread(target = receive)

sendThread.start()
receiveThread.start()
import socket
import threading

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('192.168.55.111',55555))

def send():
    while True:
        messageOut = input('Me: ')
        client.send(messageOut.encode('utf8'))


def receive():
    while True:
        messageIn = client.recv(1024).decode('utf8')
        print(messageIn)
        

sendThread = threading.Thread(target = send)
sendThread.start()
receiveThread = threading.Thread(target = receive)
receiveThread.start()
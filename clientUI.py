# for now it has to be in the same local connection as server

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QAbstractScrollArea, QScrollArea
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import socket
import threading

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('192.168.55.111',55555))


     

class ReceiveThread(QThread):
    message_received = pyqtSignal(str)

    def run(self):
        while True:
            try:
                messageIn = client.recv(1024).decode('utf8')
                if messageIn == "NICK":
                     nick = pole_przewijane.toPlainText()
                else:
                     
                    # print(messageIn)
                    self.message_received.emit(messageIn)
                
            except ConnectionAbortedError and ConnectionResetError:
                self.message_received.emit("Stracono połączenie z serwerem")
                break

def clicked():
    
        try:
            messageOut = pole_wprowadzania.text()
            client.send(messageOut.encode('utf8'))
        except ConnectionAbortedError and ConnectionResetError:
            pole_przewijane.setPlainText(f"{pole_przewijane.toPlainText()}\nstracono połączenie z serwerem!")

def nickSendButtonClicked():
    nickOut = pole_nick.text()
    client.send(nickOut.encode('utf8'))
    okno_nick.close()
    okno_glowne.show()


app = QApplication(sys.argv)



# Tworzenie głównego okna
okno_glowne = QWidget()
okno_glowne.setWindowTitle("Group CHAT")
okno_glowne.setGeometry(400, 400, 600, 600)
okno_glowne.move(100,100)

# Okno dla nicku
okno_nick = QWidget()
okno_nick.setWindowTitle("Group CHAT")
okno_nick.setGeometry(100, 100, 550, 100)
okno_nick.move(100, 100)

# Pole tekstowe na nick
pole_nick = QLineEdit(okno_nick)
pole_nick.setGeometry(10, 10, 200, 30)
pole_nick.setPlaceholderText("Wprowadź swój nick")

# Przycisk
przycisk = QPushButton("OK", okno_nick)
przycisk.clicked.connect(nickSendButtonClicked)
przycisk.setGeometry(220, 10, 60, 30)



# Układ wertykalny dla komponentów
uklad = QVBoxLayout()

# Tworzenie nieedytowalnego pola przewijanego
pole_przewijane = QTextEdit()
pole_przewijane.setGeometry(400, 400, 550, 485)
pole_przewijane.setPlainText("-------------------------------")
pole_przewijane.setReadOnly(True)
scroll_area = QScrollArea()
scroll_area.setWidget(pole_przewijane)

# Tworzenie pola do wprowadzania tekstu
pole_wprowadzania = QLineEdit()

# Tworzenie przycisku
przycisk = QPushButton("WYSLIJ")
przycisk.clicked.connect(clicked)

# Dodawanie komponentów do układu
uklad.addWidget(scroll_area)
uklad.addWidget(pole_wprowadzania)
uklad.addWidget(przycisk)

receive_thread = ReceiveThread()
receive_thread.message_received.connect(lambda message: pole_przewijane.setPlainText(f"{pole_przewijane.toPlainText()}\n{message}"))
receive_thread.start()


okno_glowne.setLayout(uklad)

okno_nick.show()


sys.exit(app.exec_())







import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QAbstractScrollArea, QScrollArea
import socket
import threading

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('192.168.55.111',55555))



def pole_przewijane_update(messageIn):
    print(messageIn)
    pole_przewijane.setPlainText(f"{pole_przewijane.toPlainText()}\n{messageIn}")

def clicked():
    
    try:
        messageOut = pole_wprowadzania.text()
        client.send(messageOut.encode('utf8'))
    except ConnectionAbortedError and ConnectionResetError:
            pole_przewijane.setPlainText(f"{pole_przewijane.toPlainText()}\nstracono połączenie z serwerem!")
            
def receive():
    while True:
        try:
            messageIn = client.recv(1024).decode('utf8')
            print(messageIn)
            pole_przewijane_update(messageIn)
        except ConnectionAbortedError and ConnectionResetError:
            # pole_przewijane.setPlainText(f"{pole_przewijane.toPlainText()}\nStracono połączenie z serwerem")
            break

receiveThread = threading.Thread(target = receive)
receiveThread.start()

app = QApplication(sys.argv)



# Tworzenie głównego okna
okno_glowne = QWidget()
okno_glowne.setWindowTitle("Group CHAT")
okno_glowne.setGeometry(400, 400, 600, 600)

# Układ wertykalny dla komponentów
uklad = QVBoxLayout()

# Tworzenie nieedytowalnego pola przewijanego
pole_przewijane = QTextEdit()
pole_przewijane.setGeometry(400, 400, 550, 485)
pole_przewijane.setPlainText("--")
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




okno_glowne.setLayout(uklad)

okno_glowne.show()
sys.exit(app.exec_())







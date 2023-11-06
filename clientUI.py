# for now it has to be in the same local connection as server

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QAbstractScrollArea, QScrollArea
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import socket
import threading

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)



class ReceiveThread(QThread):
    message_received = pyqtSignal(str)

    def run(self):
        while True:
            try:
                message_in = client.recv(1024).decode('utf8')
                self.message_received.emit(message_in)
                
            except ConnectionAbortedError and ConnectionResetError:
                self.message_received.emit("Stracono połączenie z serwerem")
                break

def clicked():
    
        try:
            message_out = message_input_field.text()
            client.send(message_out.encode('utf8'))
            message_input_field.clear()
        except ConnectionAbortedError and ConnectionResetError:
            chat_area.setPlainText(f"{chat_area.toPlainText()}\nstracono połączenie z serwerem!")

def nickSendButtonClicked():


    nick_out = nick_field.text()
    client.connect(('192.168.55.111',55555))
    client.send(nick_out.encode('utf8'))
    
    receive_thread = ReceiveThread()
    receive_thread.message_received.connect(lambda message: chat_area.setPlainText(f"{chat_area.toPlainText()}\n{message}"))
    receive_thread.start()

    
    login_window.close()
    main_window.show()
    chat_area.setPlainText(f"{nick_out}\n\n{chat_area.toPlainText()}")
    main_window.setWindowTitle(f"Group CHAT [{nick_out}]")


app = QApplication(sys.argv)


# Okno dla nicku:
login_window = QWidget()
login_window.setWindowTitle("Group CHAT")
login_window.setGeometry(100, 100, 550, 100)
login_window.move(100, 100)

# Pole tekstowe na nick
nick_field = QLineEdit(login_window)
nick_field.setGeometry(10, 10, 200, 30)
nick_field.setPlaceholderText("Wprowadź swój nick")

# Przycisk
login_button = QPushButton("OK", login_window)
login_button.clicked.connect(nickSendButtonClicked)
login_button.setGeometry(220, 10, 60, 30)



# Okno główne:
main_window = QWidget()
main_window.setWindowTitle("Group CHAT")
main_window.setGeometry(400, 400, 600, 600)
main_window.move(100,100)

# Układ wertykalny dla komponentów
layout = QVBoxLayout()

# Tworzenie nieedytowalnego pola przewijanego
chat_area = QTextEdit()
chat_area.setGeometry(400, 400, 550, 485)
chat_area.setPlainText("-------------------------------")
chat_area.setReadOnly(True)
scroll_area = QScrollArea()
scroll_area.setWidget(chat_area)

# Tworzenie pola do wprowadzania tekstu
message_input_field = QLineEdit()

# Tworzenie przycisku
message_button = QPushButton("WYSLIJ")
message_button.clicked.connect(clicked)

# Dodawanie komponentów do układu
layout.addWidget(scroll_area)
layout.addWidget(message_input_field)
layout.addWidget(message_button)




main_window.setLayout(layout)

login_window.show()

sys.exit(app.exec_())







# for now it has to be in the same local connection as server

import sys
from PyQt5.QtWidgets import QMainWindow, QComboBox, QMenu,QMenuBar, QStatusBar, QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QAbstractScrollArea, QScrollArea, QToolBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QRect, QMetaObject, QCoreApplication, QMetaObject
from PyQt5.QtGui import QValidator
import socket
import threading

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_ip = '192.168.55.111'

receive_thread = None


class NoLeadingDigitValidator(QValidator):
    def validate(self, input_str, pos):
        if input_str and input_str[0].isdigit():
            return (QValidator.Invalid, input_str, pos)
        return (QValidator.Acceptable, input_str, pos)

class ReceiveThread(QThread):
    message_received = pyqtSignal(str)
    db_message_received = pyqtSignal(str)
    
    def run(self):
        while True:
            
            try:
                message_in = client.recv(4096).decode('utf8','ignore')
                if message_in.startswith("[NDB]"):
                    message_in = message_in[5:]
                    # print(message_in)
                    self.message_received.emit(message_in)
                elif message_in.startswith("[DB]"):
                    self.db_message_received.emit(message_in)
                    
                
            except ConnectionAbortedError and ConnectionResetError:
                self.message_received.emit("Stracono połączenie z serwerem")
                break


def searching_clicked():
    searching_window.show()

def display_in_searching_window(message):
    searching_results_area.setPlainText(message)
    


def searching():
    
    if searching_combo_Box.currentIndex() == 0:
        all_query = f"[DB]SELECT date,nick,value FROM users,messages WHERE users.rowid = messages.user_id AND (users.nick LIKE '%{searching_line_edit.text()}%' OR messages.value LIKE '%{searching_line_edit.text()}%')"
        client.send(all_query.encode('utf8'))

    elif searching_combo_Box.currentIndex() == 1:
        user_query = f"[DB]SELECT date,nick,value FROM users,messages WHERE users.rowid = messages.user_id AND (users.nick LIKE '%{searching_line_edit.text()}%')"
        client.send(user_query.encode('utf8'))

    elif searching_combo_Box.currentIndex() == 2:
        msg_query = f"[DB]SELECT date,nick,value FROM users,messages WHERE users.rowid = messages.user_id AND (messages.value LIKE '%{searching_line_edit.text()}%')"
        client.send(msg_query.encode('utf8'))
    searching_line_edit.clear()


def clicked():
    
        try:
            message_out = '[NDB]'+message_input_field.text()
            client.send(message_out.encode('utf8'))
            message_input_field.clear()
        except ConnectionAbortedError and ConnectionResetError:
            chat_area.setPlainText(f"{chat_area.toPlainText()}\nstracono połączenie z serwerem!")

def nickSendButtonClicked():
    global receive_thread
    nick_out = nick_field.text()
    client.connect((server_ip,55555))
    client.send(nick_out.encode('utf8'))
 
    if receive_thread is None:
        receive_thread = ReceiveThread()
        receive_thread.message_received.connect(lambda message: chat_area.setPlainText(f"{chat_area.toPlainText()}\n{message}"))
        receive_thread.db_message_received.connect(lambda message: display_in_searching_window(message))
        receive_thread.start()

    login_window.close()
    main_window.show()
    chat_area.setPlainText(f"{nick_out}\n\n{chat_area.toPlainText()}")
    main_window.setWindowTitle(f"Group CHAT [{nick_out}]")



app = QApplication(sys.argv)

###############################################################################################
# window for nick:
login_window = QWidget()
login_window.setWindowTitle("Group CHAT")
login_window.setGeometry(100, 100, 550, 100)
login_window.move(100, 100)

# textfield for nick
nick_field = QLineEdit(login_window)
nick_field.setGeometry(10, 10, 420, 30)
nick_field.setPlaceholderText("Wprowadź swój nick (Nie może zaczynać się od cyfry!)")


#Validator for the nickname input field that disallows adding digits as the first character, which could interfere with assigning IDs on the server side.
validator = NoLeadingDigitValidator()
nick_field.setValidator(validator)

# button for nick
login_button = QPushButton("OK", login_window)
login_button.clicked.connect(nickSendButtonClicked)
login_button.setGeometry(450, 10, 60, 30)

###########################################################################################

# Window for searching:

searching_window = QWidget()


searching_window.setObjectName("Wyszukiwanie")
searching_window.resize(500, 574)
searching_window.setWindowTitle("Wyszukiwanie w czacie")


searching_combo_Box = QComboBox(searching_window)
searching_combo_Box.setGeometry(QRect(10, 20, 280, 30))
searching_combo_Box.setObjectName("comboBox")
searching_combo_Box.addItem("Wyszukiwanie ogólne")
searching_combo_Box.addItem("Wyszukiwanie po użytkowniku")
searching_combo_Box.addItem("Wyszukiwanie po wiadomości")

searching_line_edit = QLineEdit(searching_window)
searching_line_edit.setGeometry(QRect(10, 55, 310, 30))
searching_line_edit.setObjectName("lineEdit")

searching_push_button = QPushButton(searching_window)
searching_push_button.setGeometry(QRect(328, 55, 100, 32))
searching_push_button.setObjectName("pushButton")
searching_push_button.setText("Wyszukaj")
searching_push_button.clicked.connect(searching)

searching_results_area = QTextEdit(searching_window)
searching_results_area.setGeometry(10, 100, 430, 430)
searching_results_area.setPlainText("-------------------------------")
searching_results_area.setReadOnly(True)


scrollArea = QScrollArea(searching_window)
scrollArea.setGeometry(10, 100, 430, 430)


scrollArea.setWidget(searching_results_area)


# ##################################################################################

# main window:
main_window = QWidget()
main_window.setWindowTitle("Group CHAT")
main_window.setGeometry(400, 400, 600, 600)
main_window.move(100,100)



# layout for components
layout = QVBoxLayout()

# creating uneditable scrolling area
chat_area = QTextEdit()
chat_area.setGeometry(400, 400, 550, 485)
chat_area.setPlainText("-------------------------------")
chat_area.setReadOnly(True)
scroll_area = QScrollArea()
scroll_area.setWidget(chat_area)

# creating field to input text
message_input_field = QLineEdit()

# creating button
message_button = QPushButton("WYSLIJ")
message_button.clicked.connect(clicked)
search_button = QPushButton("WYSZUKAJ WIADOMOŚCI")
search_button.clicked.connect(searching_clicked)

# adding components to layout
layout.addWidget(search_button)
layout.addWidget(scroll_area)
layout.addWidget(message_input_field)
layout.addWidget(message_button)


main_window.setLayout(layout)

login_window.show()

sys.exit(app.exec_())







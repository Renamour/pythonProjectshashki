import ast

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

import cipher

from tkinter import Tk, Canvas, PhotoImage
from checkers.game import Game
from checkers.constants import X_SIZE, Y_SIZE, CELL_SIZE


class SignUp(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent_dialog = parent
        self.setWindowTitle("Sign up")
        self.setFixedSize(600, 400)
        self.def_font = QtGui.QFont()
        self.def_font.setFamily("Tahoma")
        self.def_font.setPixelSize(25)
        self.def_font.setBold(True)
        self.def_font.setItalic(False)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, 600, 90))
        self.label.setFont(self.def_font)
        self.label.setObjectName("label")
        self.label.setText("Регистрация")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.loginInput = QtWidgets.QLineEdit(self)
        self.loginInput.setGeometry(QtCore.QRect(120, 100, 360, 35))
        self.loginInput.setObjectName("loginInput")
        self.loginInput.setPlaceholderText("Имя пользователя")

        self.passInput = QtWidgets.QLineEdit(self)
        self.passInput.setGeometry(QtCore.QRect(120, 150, 360, 35))
        self.passInput.setObjectName("passInput")
        self.passInput.setPlaceholderText("Пароль")

        self.rpassInput = QtWidgets.QLineEdit(self)
        self.rpassInput.setGeometry(QtCore.QRect(120, 200, 360, 35))
        self.rpassInput.setObjectName("rpassInput")
        self.rpassInput.setPlaceholderText("Повторите пароль")

        self.signupBtn = QtWidgets.QPushButton(self)
        self.signupBtn.setGeometry(QtCore.QRect(200, 250, 200, 45))
        self.signupBtn.setText("Зарегистрироваться")

        self.backtologin = QtWidgets.QPushButton(self)
        self.backtologin.setGeometry(QtCore.QRect(200, 300, 200, 45))
        self.backtologin.setText("Я уже зарегистрирован")

        self.registerBtns()

    @QtCore.pyqtSlot()
    def registerBtnHandler(self):
        if self.loginInput.text() and self.passInput.text() and self.rpassInput.text():
            login = self.loginInput.text()
            password = self.passInput.text()
            rpassword = self.rpassInput.text()
            if password == rpassword:
                with open('login.txt', 'r+') as f:
                    data = f.read()
                accounts = []
                if data is not None:
                    rows = data.split('\n')
                    if len(rows) > 1:
                        if len(rows) != 0:
                            accounts = [x.split() for x in rows]
                if len(accounts) != 0:
                    find = False
                    for acc in accounts:
                        if len(acc) >= 2:
                            if acc[0] == login:
                                find = True
                    if find:
                        QtWidgets.QMessageBox.information(self, 'Внимание!', 'Пользователь с таким именем уже существует')
                    else:
                        with open('login.txt', 'a+') as f:
                            account_row = [login.replace(' ', ''), cipher.encrypt(password, cipher.APP_RSA_PUBLIC_KEY)]
                            f.write(str(account_row) + "\n")
                        self.close()
                else:
                    with open('login.txt', 'a+') as f:
                        account_row = [login.replace(' ', ''), cipher.encrypt(password, cipher.APP_RSA_PUBLIC_KEY)]
                        f.write(str(account_row) + "\n")
                    self.close()
            else:
                QtWidgets.QMessageBox.information(self, 'Внимание!', 'Введённые пароли не совпадают!')
        else:
            QtWidgets.QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля!')

    def tologin(self):
        self.close()
        self.parent_dialog.show()

    def registerBtns(self):
        self.signupBtn.clicked.connect(self.registerBtnHandler)
        self.backtologin.clicked.connect(self.tologin)

    def closeEvent(self, event):
        self.tologin()


class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log in")
        self.setFixedSize(600, 350)
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.def_font = QtGui.QFont()
        self.def_font.setFamily("Tahoma")
        self.def_font.setPixelSize(25)
        self.def_font.setBold(True)
        self.def_font.setItalic(False)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, 600, 90))
        self.label.setFont(self.def_font)
        self.label.setObjectName("label")
        self.label.setText("Авторизация")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.loginInput = QtWidgets.QLineEdit(self)
        self.loginInput.setGeometry(QtCore.QRect(120, 100, 360, 35))
        self.loginInput.setObjectName("loginInput")
        self.loginInput.setPlaceholderText("Имя пользователя")

        self.passInput = QtWidgets.QLineEdit(self)
        self.passInput.setGeometry(QtCore.QRect(120, 150, 360, 35))
        self.passInput.setObjectName("passInput")
        self.passInput.setPlaceholderText("Пароль")

        self.loginBtn = QtWidgets.QPushButton(self)
        self.loginBtn.setGeometry(QtCore.QRect(200, 200, 200, 45))
        self.loginBtn.setText("Войти")

        self.signupBtn = QtWidgets.QPushButton(self)
        self.signupBtn.setGeometry(QtCore.QRect(200, 250, 200, 45))
        self.signupBtn.setText("У меня нет учетной записи")

        self.registerBtns()

    @QtCore.pyqtSlot()
    def registerBtnHandler(self):
        self.hide()
        self.sign_up_wind = SignUp(self)
        self.sign_up_wind.show()

    @QtCore.pyqtSlot()
    def loginBtnHandler(self):
        login = self.loginInput.text()
        password = self.passInput.text()
        if not login or not password:
            QtWidgets.QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля!')
            return
        with open('login.txt', 'r') as f:
            data = f.read()
        if data is not None:
            rows = data.split('\n')
            accounts = []
            for k in rows:
                if len(k) > 0:
                    accounts.append(ast.literal_eval(k))
            account_data = None
            for k in accounts:
                if len(k) == 2:
                    if k[0] == login.replace(' ', ''):
                        account_data = k
                        break
            print(account_data)
            if account_data is not None:
                if account_data[1] == cipher.encrypt(password, cipher.APP_RSA_PUBLIC_KEY):
                    self.close()
                    run_game()
                else:
                    QtWidgets.QMessageBox.information(self, 'Внимание!', 'Неверный пароль')
            else:
                QtWidgets.QMessageBox.information(self, 'Внимание!', 'Пользователь не найден')
        else:
            QtWidgets.QMessageBox.information(self, 'Внимание!', 'Пользователь не найден')

    def registerBtns(self):
        self.signupBtn.clicked.connect(self.registerBtnHandler)
        self.loginBtn.clicked.connect(self.loginBtnHandler)


def run_game():
    main_window = Tk()
    main_window.title('Шашки')
    main_window.resizable()
    main_window.iconphoto(False, PhotoImage(file='icon.png'))

    # Создание холста
    main_canvas = Canvas(main_window, width=CELL_SIZE * X_SIZE, height=CELL_SIZE * Y_SIZE)
    main_canvas.pack()

    game = Game(main_canvas, X_SIZE, Y_SIZE)

    main_canvas.bind("<Motion>", game.mouse_move)
    main_canvas.bind("<Button-1>", game.mouse_down)

    main_window.mainloop()
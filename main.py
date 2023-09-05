import sys
from PyQt6.QtWidgets import QApplication,QMainWindow, QLabel, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from login.loginSF import LoginSF

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_up_ui()
        with open('styles/estilosMenu.css', 'r') as file:
            style = file.read()
        self.setStyleSheet(style)

    def set_up_ui(self):
        self.setGeometry(100, 100, 1024, 600)
        self.setMaximumSize(1024, 600)
        self.setWindowTitle('Menú')
        self.setWindowIcon(QIcon('img/icon.png'))
        self.show()

        self.title_label = QLabel('Bienvenido a Sound Fresh')
        self.title_label.setObjectName('title')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.account_button = QPushButton('Cuenta')
        self.account_button.setObjectName('button_account')
        self.account_button.clicked.connect(self.logSF)

        self.settings_button = QPushButton('Ajustes')
        self.settings_button.setObjectName('button_settings')
        self.settings_button.clicked.connect(self.settings)

        self.exit_button = QPushButton('Salir')
        self.exit_button.setObjectName('button_exit')
        self.exit_button.clicked.connect(self.exit)

        elements_main_v_box = QVBoxLayout()
        elements_main_v_box.addWidget(self.title_label)
        elements_main_v_box.addWidget(self.account_button)
        elements_main_v_box.addWidget(self.settings_button)
        elements_main_v_box.addWidget(self.exit_button)

        element_container = QWidget()
        element_container.setLayout(elements_main_v_box)

        self.setCentralWidget(element_container)  # Agregar el contenedor a la ventana principal

    def logSF(self):
        self.window_loginSF = LoginSF(self) # type: ignore
        self.window_loginSF.show()

    def settings(self):
        pass

    def exit(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv) # type: ignore
    main_menu = MainMenu()
    sys.exit(app.exec())
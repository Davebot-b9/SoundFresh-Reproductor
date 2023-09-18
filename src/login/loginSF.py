import sys
from pymongo import MongoClient
import bcrypt
from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QCheckBox, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt6.QtGui import QIcon
from src.login.registerSF import RegisterUserView
from src.reproductor.reprocSF import MainWindowRep

class LoginSF(QDialog):
    """Ventana de inicio de sesión de Sound Fresh."""

    def __init__(self, main_menu):
        super().__init__()
        self.setModal(True)
        self.main_menu = main_menu
        self.set_up_UI()
        self.consult_client_mongo()
        with open('styles/estilosMenu.css', 'r') as file:
            style = file.read()
        self.setStyleSheet(style)

    def set_up_UI(self):
        """Configura la interfaz de usuario de la ventana de inicio de sesión."""
        self.setGeometry(400, 300, 450, 150)
        self.setMaximumSize(450, 150)
        self.setWindowTitle('Login Sound Fresh')
        self.setWindowIcon(QIcon('img/icon.png'))
        self.generate_form()
        self.show()

    def generate_form(self):
        """Genera los elementos del formulario en la ventana."""
        self.is_logged = False

        title_login = QLabel('Login with your username and password:')
        title_login.setObjectName('title_style')
        
        #message_login.setFont(QFont('Banaue', 16, QFont.Weight.Bold))

        user_label = QLabel('User:')
        #user_label.setFont(QFont('Banaue', 12))
        user_label.setFixedWidth(80)
        user_label.setObjectName('user_style')
        self.user_input = QLineEdit()

        password_label = QLabel('Password:')
        #password_label.setFont(QFont('Banaue', 12))
        password_label.setFixedWidth(80)
        password_label.setObjectName('password_style')
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.check_view_password = QCheckBox('View Password')
        #self.check_view_password.setFont(QFont('Banaue', 12))
        self.check_view_password.setObjectName('checkbox-style')
        self.check_view_password.toggled.connect(self.view_password_sf)

        login_button = QPushButton('Login')
        #login_button.setFont(QFont('Banaue', 12, QFont.Weight.Bold))
        login_button.setFixedWidth(90)
        login_button.setObjectName('login-button-style')
        login_button.clicked.connect(self.login_user_sf)

        register_button = QPushButton('Register')
        #register_button.setFont(QFont('Banaue', 12, QFont.Weight.Bold))
        register_button.setFixedWidth(90)
        register_button.setObjectName('register-button-style')
        register_button.clicked.connect(self.register_user_sf)

        vertical_layout_main = QVBoxLayout()
        h_layout_1 = QHBoxLayout()
        h_layout_2 = QHBoxLayout()

        h_layout_1.addWidget(user_label)
        h_layout_1.addWidget(self.user_input)

        h_layout_2.addWidget(password_label)
        h_layout_2.addWidget(self.password_input)

        vertical_layout_main.addWidget(title_login)
        vertical_layout_main.addLayout(h_layout_1)
        vertical_layout_main.addLayout(h_layout_2)
        vertical_layout_main.addWidget(self.check_view_password)

        button_layout = QHBoxLayout()
        button_layout.addWidget(login_button)
        button_layout.addWidget(register_button)

        vertical_layout_main.addLayout(button_layout)

        self.setLayout(vertical_layout_main)

    def view_password_sf(self, clicked):
        """Cambia el modo de visualización de la contraseña según el estado de la casilla de verificación."""
        self.password_input.setEchoMode(QLineEdit.EchoMode.Normal) if clicked else self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def consult_client_mongo(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client["RegisterSound"]
        self.collection = self.db["SounsFreshUsers"]
        
    def login_user_sf(self):
        """Función para el inicio de sesión del usuario."""
        username_login = self.user_input.text()
        password_login = self.password_input.text()

        try:
            user_data = self.collection.find_one({"username": username_login})
            if user_data:
                hashed_password_db = user_data["hashed_password"]

                if bcrypt.checkpw(password_login.encode('utf-8'), hashed_password_db):
                    QMessageBox.information(self, "Login Success",
                    "Login successful", QMessageBox.StandardButton.Ok,
                    QMessageBox.StandardButton.Ok
                    )
                    self.is_logged = True
                    self.main_menu.close()
                    self.open_main_window()
                    self.close()
                else:
                    QMessageBox.warning(self, "Login Failed", "Incorrect credentials", QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
            else:
                QMessageBox.warning(self, "Login Failed", "User not found", QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)

        except FileNotFoundError as e:
            QMessageBox.warning(self, "Error BD", f"Base de datos de usuario no encontrada: {e}", QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
        except Exception as e:
            QMessageBox.warning(self, "Error Servidor", f"Error en el servidor: {e}", QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)

    def register_user_sf(self):
        """Abre la ventana de registro de usuario al hacer clic en el botón de registro."""
        self.new_user_form_sf = RegisterUserView()
        self.new_user_form_sf.show()

    def open_main_window(self):
        """Abre la ventana principal después de un inicio de sesión exitoso."""
        self.reproductor_window = MainWindowRep()
        self.reproductor_window.show()
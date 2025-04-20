
import sys
import sqlite3
import bcrypt
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QCheckBox, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt6.QtGui import QIcon
from src.login.registerSF import RegisterUserView
from src.reproductor.reprocSF import MainWindowRep
from src.database.db_setup import get_db_connection # Import SQLite connection function

class LoginSF(QDialog):
    """Ventana de inicio de sesión de Sound Fresh."""

    def __init__(self, main_menu):
        super().__init__()
        self.setModal(True)
        self.main_menu = main_menu # Assuming main_menu is the parent window that might need closing
        self.logged_in_user_id = None # Variable to store user_id after login
        self.set_up_UI()
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

        user_label = QLabel('User:')
        user_label.setFixedWidth(80)
        user_label.setObjectName('user_style')
        self.user_input = QLineEdit()

        password_label = QLabel('Password:')
        password_label.setFixedWidth(80)
        password_label.setObjectName('password_style')
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.check_view_password = QCheckBox('View Password')
        self.check_view_password.setObjectName('checkbox-style')
        self.check_view_password.toggled.connect(self.view_password_sf)

        login_button = QPushButton('Login')
        login_button.setFixedWidth(90)
        login_button.setObjectName('login-button-style')
        login_button.clicked.connect(self.login_user_sf)

        register_button = QPushButton('Register')
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

    def login_user_sf(self):
        """Función para el inicio de sesión del usuario usando SQLite."""
        username_login = self.user_input.text()
        password_login = self.password_input.text()

        if not username_login or not password_login:
            QMessageBox.warning(self, "Login Failed", "Please enter username and password", 
                                QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
            return

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Find user by username
            cursor.execute("SELECT user_id, username, hashed_password FROM users WHERE username = ?", (username_login,))
            user_data = cursor.fetchone() # Fetch one record
            
            if user_data: # If user exists
                stored_hashed_password = user_data["hashed_password"] # Access by column name
                
                # Check the password
                if bcrypt.checkpw(password_login.encode('utf-8'), stored_hashed_password):
                    # Password matches
                    self.is_logged = True
                    self.logged_in_user_id = user_data["user_id"] # Store the user_id
                    
                    QMessageBox.information(self, "Login Success", "Login successful", 
                                            QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)

                    if self.main_menu:
                         self.main_menu.close() # Close the previous window (assuming it's the main menu)
                    self.open_main_window()
                    self.accept() # Use accept() for successful dialog close
                else:
                    # Incorrect password
                    QMessageBox.warning(self, "Login Failed", "Incorrect credentials", 
                                        QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
            else:
                # User not found
                QMessageBox.warning(self, "Login Failed", "User not found", 
                                    QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)

        except sqlite3.Error as e:
            QMessageBox.warning(self, "Database Error", f"Error accessing database: {e}", 
                                QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An unexpected error occurred: {e}", 
                                QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
        finally:
            if conn:
                conn.close()

    def register_user_sf(self):
        """Abre la ventana de registro de usuario al hacer clic en el botón de registro."""
        self.new_user_form_sf = RegisterUserView()
        self.new_user_form_sf.exec() # Use exec() for modal dialog behavior

    def open_main_window(self):
        """Abre la ventana principal después de un inicio de sesión exitoso."""
        if self.logged_in_user_id:
            # Pass the user_id to the main window
            self.reproductor_window = MainWindowRep(user_id=self.logged_in_user_id) 
            self.reproductor_window.show()
        else:
             # Should not happen if login was successful, but good to handle
             QMessageBox.critical(self, "Error", "Could not open main window: User ID not found.",
                                 QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)


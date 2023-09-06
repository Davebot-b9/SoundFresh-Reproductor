from pymongo import MongoClient
import bcrypt
import datetime
from PyQt6 import QtCore
from PyQt6.QtWidgets import (QLabel, QPushButton, QDateEdit, QLineEdit,
                            QComboBox, QFormLayout, QHBoxLayout, QMessageBox, QDialog)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QDate
from login.constants import city, gender


class RegisterUserView(QDialog):
    def __init__(self):
        super().__init__()
        self.setModal(True)  # type: ignore
        self.initialize_ui()
        with open('styles/estilosMenu.css', 'r') as file:
            style = file.read()
        self.setStyleSheet(style)
        self.retrieve_user_data()

    def initialize_ui(self):
        # Configurar el tamaño, título y ícono de la ventana de registro
        self.setGeometry(400, 300, 450, 250)
        self.setMaximumSize(450, 250)
        self.setWindowTitle('Register Sound Fresh')
        self.setWindowIcon(QIcon('img/icon.png'))
        self.generate_form()

    def generate_form(self):

        message_register = QLabel('Registra todos tus datos:')
        message_register.setObjectName('message-style')
        message_register.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Name
        name_label = QLabel('Name:')
        name_label.setObjectName('name-label-style')
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")

        # Lastname
        lastname_label = QLabel('Lastname:')
        lastname_label.setObjectName('lastname-label-style')
        self.lastname_input = QLineEdit()
        self.lastname_input.setPlaceholderText("Lastname")

        # Age
        age_label = QLabel('Age:')
        age_label.setObjectName('age-label-style')
        self.date_edit = QDateEdit()
        self.date_edit.setDisplayFormat("dd-MM-yyyy")
        self.date_edit.setMaximumDate(
            QDate.currentDate()
        )
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        # gender
        gender_label = QLabel('Gender:')
        gender_label.setObjectName('gender-label-style')
        self.gender_selection = QComboBox()
        self.gender_selection.addItems(gender)

        # city
        city_label = QLabel('Country:')
        city_label.setObjectName('city-label-style')
        self.city_selection = QComboBox()
        self.city_selection.addItems(city)

        # User
        user_label = QLabel('User:')
        user_label.setObjectName('user-label-style')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("User")

        # email
        email_label = QLabel('E-mail:')
        email_label.setObjectName('email-label-style')
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-mail")

        # password
        password_label = QLabel('Pasword:')
        password_label.setObjectName('password-label-style')
        self.password = QLineEdit()
        self.password.setPlaceholderText("12345")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        # confirm password
        confirm_password_label = QLabel('Confirm Password:')
        confirm_password_label.setObjectName('confirm-label-style')
        self.password_confirm = QLineEdit()
        self.password_confirm.setPlaceholderText("12345")
        self.password_confirm.setEchoMode(QLineEdit.EchoMode.Password)

        create_button = QPushButton('Confirm')
        create_button.setObjectName('create-button-style')
        create_button.clicked.connect(self.create_user)

        cancel_button = QPushButton('Cancel')
        cancel_button.setObjectName('cancel-button-style')
        cancel_button.clicked.connect(self.cancel_register)

        main_button = QHBoxLayout()
        main_button.addWidget(create_button)
        main_button.addWidget(cancel_button)

        main_form = QFormLayout()
        main_form.addRow(message_register)
        main_form.addRow(name_label, self.name_input)
        main_form.addRow(lastname_label, self.lastname_input)
        main_form.addRow(age_label, self.date_edit)
        main_form.addRow(gender_label, self.gender_selection)
        main_form.addRow(city_label, self.city_selection)
        main_form.addRow(user_label, self.username_input)
        main_form.addRow(email_label, self.email_input)
        main_form.addRow(password_label, self.password)
        main_form.addRow(confirm_password_label, self.password_confirm)
        main_form.addItem(main_button)

        self.setLayout(main_form)

    def cancel_register(self):
        self.close()

    def calculate_age(self):
        fecha_nacimiento = self.date_edit.date()
        fecha_actual = QDate.currentDate()
        age = fecha_actual.year() - fecha_nacimiento.year()
        # if fecha_actual.month < fecha_nacimiento.month or (fecha_actual.month ==  fecha_nacimiento.month and fecha_actual.day < fecha_nacimiento.day):
        #     age -= 1
        return age

    def retrieve_user_data(self):
        # URL connection db
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["RegisterSound"]  # Name Database
        self.collection = self.db["SounsFreshUsers"]  # Name Collection

        cursor = self.collection.find({})

        for document in cursor:
            name_db = document["name"]
            last_name_db = document["last_name"]
            age_db = document["age"]
            gender_db = document["gender"]
            country_db = document["country"]
            username_db = document["username"]
            email_db = document["email"]
            hashed_password_db = document["hashed_password"]
            registration_date_db = document["registration_date"]

    def create_user(self):
        user_sf = self.username_input.text()
        password_sf = self.password.text()
        hashed_password = bcrypt.hashpw(password_sf.encode('utf-8'), bcrypt.gensalt())
        confirm_sf = self.password_confirm.text()
        registration_date = datetime.datetime.now()

        if not (password_sf and confirm_sf and user_sf):
            QMessageBox.warning(self, 'Error',
            'Please enter valid data',
            QMessageBox.StandardButton.Close,
            QMessageBox.StandardButton.Close)
        elif password_sf != confirm_sf:
            QMessageBox.warning(self, 'Error',
            'Passwords do not match',
            QMessageBox.StandardButton.Close,
            QMessageBox.StandardButton.Close)
        else:
            try:
                # Validación de usuario y contraseña
                if len(user_sf) > 10:
                    QMessageBox.warning(self, 'Error',
                    'Username must be up to 10 characters',
                    QMessageBox.StandardButton.Close,
                    QMessageBox.StandardButton.Close)
                elif not (user_sf.isalnum() and user_sf.isascii()):
                    QMessageBox.warning(self, 'Error',
                    'Username can only contain letters and numbers',
                    QMessageBox.StandardButton.Close,
                    QMessageBox.StandardButton.Close)
                elif not (8 <= len(password_sf) <= 20 and any(c.isdigit() for c in password_sf) and any(c.isupper() for c in password_sf) and any(not c.isalnum() for c in password_sf)):
                    QMessageBox.warning(self, 'Error', 
                    'Password must be 8-20 characters long and include at least one uppercase letter, one digit, and one special character',
                    QMessageBox.StandardButton.Close, 
                    QMessageBox.StandardButton.Close)
                else:
                    # Validación de nombre y apellido (name_sf y lastname_sf)
                    if not (self.name_input.text().isalpha() and self.lastname_input.text().isalpha()):
                        QMessageBox.warning(self, 'Error', 'Name and lastname can only contain letters',
                                            QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
                    else:
                        # Validación de edad (age_sf)
                        min_age = QDate.currentDate().addYears(-18)
                        if self.date_edit.date() > min_age:
                            QMessageBox.warning(self, 'Error',
                                                'You must be 18 years old or older to register',
                                                QMessageBox.StandardButton.Close,
                                                QMessageBox.StandardButton.Close)
                        else:
                            # Validación de email (email_sf)
                            valid_email_domains = [
                                '@gmail.com', '@outlook.com', '@hotmail.com']
                            if not any(domain in self.email_input.text() for domain in valid_email_domains):
                                QMessageBox.warning(self, 'Error',
                                'Invalid email format. Please use @gmail.com, @outlook.com, or @hotmail.com',
                                QMessageBox.StandardButton.Close,
                                QMessageBox.StandardButton.Close)
                            else:
                                # Resto del proceso de creación de usuario
                                # Utiliza los datos recuperados de la base de datos en lugar de user_sf y otros
                                new_user = {
                                    "name": self.name_input.text(),
                                    "last_name": self.lastname_input.text(),
                                    "age": self.calculate_age(),
                                    "gender": self.gender_selection.currentText(),
                                    "country": self.city_selection.currentText(),
                                    "username": self.username_input.text(),
                                    "email": self.email_input.text(),
                                    "hashed_password": hashed_password,
                                    "registration_date": registration_date
                                }

                                # Inserta el nuevo usuario en la base de datos
                                self.collection.insert_one(new_user)
                                QMessageBox.information(self, 
                                'Successful Registration',
                                'User created successfully',
                                QMessageBox.StandardButton.Ok,
                                QMessageBox.StandardButton.Ok)
                                
                                self.close()
            except FileNotFoundError as e:
                QMessageBox.warning(self, 'Error',
                                    f'User database not found: {e}',
                                    QMessageBox.StandardButton.Close,
                                    QMessageBox.StandardButton.Close)


import sys
import sqlite3
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout, QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal # Import pyqtSignal
from src.database.db_setup import get_db_connection # Import SQLite connection function

class FormListMusic(QDialog):
    # Signal emitted when a playlist is successfully saved
    playlist_saved = pyqtSignal()
    
    def __init__(self, user_id=None, current_songs=None):
        super().__init__()
        self.setModal(True)
        self.songs_to_save = current_songs if current_songs else [] # Get songs from main window
        self.user_id = user_id # Get user_id from main window
        self.set_up_UI()
        with open('styles/estilosMenu.css', 'r') as file:
            style = file.read()
        self.setStyleSheet(style)
    
    def set_up_UI(self):
        self.setGeometry(400, 300, 400, 120) # Adjusted size
        self.setMaximumSize(400, 120)
        self.setWindowTitle('Guardar Nueva Playlist')
        self.setWindowIcon(QIcon('img/icon.png'))
        self.generate_form_playlist()
        # self.show() # Show is called by exec() in MainWindowRep
    
    def generate_form_playlist(self):
        layout = QVBoxLayout()
        form_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        # Label y campo de texto para el nombre de la playlist
        label_name = QLabel('Nombre:')
        self.text_name = QLineEdit()
        self.text_name.setPlaceholderText("Ej: Mi Playlist Favorita")
        
        form_layout.addWidget(label_name)
        form_layout.addWidget(self.text_name)
        
        form_container = QWidget()
        form_container.setLayout(form_layout)

        # Botón para guardar la playlist
        save_button = QPushButton('Guardar')
        save_button.setObjectName('save-playlist-button') # Add style if needed
        save_button.clicked.connect(self.save_new_playlist)
        
        cancel_button = QPushButton('Cancelar')
        cancel_button.setObjectName('cancel-playlist-button') # Add style if needed
        cancel_button.clicked.connect(self.cancel_new_playlist)
        
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        button_layout.addStretch()
        
        button_container = QWidget()
        button_container.setLayout(button_layout)

        layout.addWidget(form_container)
        layout.addWidget(button_container)

        self.setLayout(layout)

    def save_new_playlist(self):
        playlist_name = self.text_name.text().strip() # Remove leading/trailing whitespace
        
        # --- Input Validation --- 
        if not playlist_name:
            QMessageBox.warning(self, "Nombre Vacío", "Por favor, introduce un nombre para la playlist.", QMessageBox.StandardButton.Ok)
            return
            
        if not self.user_id:
            QMessageBox.critical(self, 'Error', 'Error interno: No se pudo identificar al usuario.', QMessageBox.StandardButton.Ok)
            return
            
        if not self.songs_to_save:
            QMessageBox.warning(self, "Lista Vacía", "No hay canciones en la lista actual para guardar.", QMessageBox.StandardButton.Ok)
            return
        
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if playlist name already exists for this user
            cursor.execute("SELECT playlist_id FROM playlists WHERE user_id = ? AND name_playlist = ?", (self.user_id, playlist_name))
            if cursor.fetchone():
                QMessageBox.warning(self, "Nombre Duplicado", f'Ya tienes una playlist llamada "{playlist_name}". Por favor elige otro nombre.', QMessageBox.StandardButton.Ok)
                return

            # --- Save to Database --- 
            # 1. Insert into playlists table
            cursor.execute("INSERT INTO playlists (user_id, name_playlist) VALUES (?, ?)", (self.user_id, playlist_name))
            new_playlist_id = cursor.lastrowid # Get the ID of the newly inserted playlist
            
            # 2. Insert into playlist_songs table
            songs_data = [(new_playlist_id, song_path) for song_path in self.songs_to_save]
            cursor.executemany("INSERT INTO playlist_songs (playlist_id, song_path) VALUES (?, ?)", songs_data)
            
            conn.commit() # Commit the transaction
            
            QMessageBox.information(self, 'Éxito', f'Playlist "{playlist_name}" guardada correctamente.', QMessageBox.StandardButton.Ok)
            self.playlist_saved.emit() # Emit the signal
            self.accept() # Close the dialog successfully

        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Error de Base de Datos', f'No se pudo guardar la playlist: {e}', QMessageBox.StandardButton.Ok)
            if conn: conn.rollback() # Rollback changes on error
        except Exception as e:
            QMessageBox.critical(self, 'Error Inesperado', f'Ocurrió un error inesperado: {e}', QMessageBox.StandardButton.Ok)
            if conn: conn.rollback()
        finally:
            if conn:
                conn.close() # Ensure connection is closed
    
    def cancel_new_playlist(self):
        self.reject() # Close the dialog without saving

# Example usage (for testing if needed)
# if __name__ == '__main__':
#     # Need to initialize DB first for testing
#     from src.database.db_setup import initialize_database
#     initialize_database()
#     app = QApplication(sys.argv)
#     # Provide dummy data for testing
#     dummy_songs = ["/path/to/song1.mp3", "/path/to/song2.mp3"]
#     dummy_user_id = 1 # Assuming a user with ID 1 exists from registration testing
#     form = FormListMusic(user_id=dummy_user_id, current_songs=dummy_songs)
#     form.show()
#     sys.exit(app.exec())

import sys
from pymongo import MongoClient
from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt6.QtGui import QIcon

class FormListMusic(QDialog):
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.songs = []
        self.set_up_UI()
        with open('styles/estilosMenu.css', 'r') as file:
            style = file.read()
        self.setStyleSheet(style)
    
    def set_up_UI(self):
        self.setGeometry(400, 300, 450, 150)
        self.setMaximumSize(450, 150)
        self.setWindowTitle('Form new playlist')
        self.setWindowIcon(QIcon('img/icon.png'))
        self.generate_form_playlist()
        self.show()
    
    def generate_form_playlist(self):
        layout = QVBoxLayout()
        # Label y campo de texto para el nombre de la playlist
        label_name = QLabel('Nombre de la Playlist:')
        self.text_name = QLineEdit()
        layout.addWidget(label_name)
        layout.addWidget(self.text_name)

        # Botón para guardar la playlist
        save_button = QPushButton('Guardar Playlist')
        save_button.clicked.connect(self.save_new_playlist)
        cancel_button = QPushButton('Cancelar')
        cancel_button.clicked.connect(self.cancel_new_playlist)
        
        layout.addWidget(save_button)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def save_new_playlist(self):
        self.is_save_playlist = False
        # Obtén el nombre de la playlist
        playlist_name = self.text_name.text()
        
        # Obtén la lista de canciones que deseas agregar a la playlist
        save_songs = self.songs  # Debes llenar esta lista con las canciones seleccionadas
        # Conecta a la base de datos MongoDB
        client = MongoClient('mongodb://localhost:27017/')  # Cambia la URL según tu configuración
        db = client['SongsFresh'] 
        collection = db['PlaylistUsers'] 
        
        # Guarda la información en la colección de MongoDB
        playlist_data = {
            'name_playlist': playlist_name,
            'songs': save_songs
        }
        try:
            result = collection.insert_one(playlist_data)
            if result.inserted_id:
                QMessageBox.information(self, 'Éxito', f'Playlist "{playlist_name}" guardada correctamente en la base de datos.', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
                self.text_name.clear()  # Limpia el campo de texto
                self.is_save_playlist = True
                self.close()
            else:
                QMessageBox.critical(self, 'Error', 'Hubo un error al guardar la playlist en la base de datos.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error al guardar la playlist en la base de datos: {str(e)}')
        finally:
            client.close()  # Cierra la conexión a MongoDB
    
    def cancel_new_playlist(self):
        self.close()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     form = FormListMusic()
#     sys.exit(app.exec())
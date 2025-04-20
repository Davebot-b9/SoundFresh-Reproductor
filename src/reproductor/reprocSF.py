
import os
import random
import sys
import sqlite3
from PyQt6.QtCore import QStandardPaths, Qt, QUrl
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QPixmap
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import (QApplication, QDockWidget, QFileDialog,
                            QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
                            QMainWindow, QMessageBox, QPushButton, QStatusBar,
                            QTabWidget, QVBoxLayout, QWidget)

from .form_playlist import FormListMusic
# Import SQLite connection function
from src.database.db_setup import get_db_connection


class MainWindowRep(QMainWindow):
    def __init__(self, user_id=None):  # Accept user_id
        super().__init__()
        self.current_user_id = user_id  # Store user_id
        self.initialize_ui()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.current_music_folder = ""
        with open('styles/estilosRep.css', 'r') as file:
            style = file.read()
        self.setStyleSheet(style)
        self.song_list = []  # Initialize an empty list to store songs
        self.player = None
        self.playing_reproductor = False
        self.current_index = -1
        self.current_position = 0
        self.is_random = False
        self.is_repeat = False
        self.load_user_playlists()  # Load playlists when window opens

    def initialize_ui(self):
        self.setGeometry(100, 100, 1020, 600)
        self.setMaximumWidth(1020)
        self.setWindowTitle('Sound Fresh - Reproductor')
        self.setWindowIcon(QIcon('img/icon.png'))
        self.generate_main_window()
        self.create_dock()
        self.create_action()
        self.create_menu()
        self.show()

    def generate_main_window(self):
        tab_bar = QTabWidget(self)
        self.reproductor_container = QWidget()
        self.playlist_saved_user = QWidget()  # Library Tab
        self.settings_container = QWidget()
        tab_bar.addTab(self.reproductor_container, "Reproductor")
        tab_bar.addTab(self.playlist_saved_user, "Biblioteca")
        tab_bar.addTab(self.settings_container, "Ajustes")
        self.generate_repro_tab()
        self.generate_playlist_user_tab()  # Renamed for clarity
        self.generate_settings_tab()

        tab_h_box = QHBoxLayout()
        tab_h_box.addWidget(tab_bar)

        main_container = QWidget()
        main_container.setLayout(tab_h_box)
        self.setCentralWidget(main_container)

    def generate_repro_tab(self):
        # ... (Reproducer tab UI remains the same) ...
        main_v_box = QVBoxLayout()
        buttons_h_box = QHBoxLayout()

        song_image = QLabel()
        pixmap = QPixmap("img/disc.jpg")
        song_image.setPixmap(pixmap)
        song_image.setScaledContents(True)

        self.button_random = QPushButton()
        self.button_random.clicked.connect(self.random_mode_toggle)
        self.button_random.setObjectName('button_random')

        button_before = QPushButton()
        button_before.clicked.connect(self.play_previous_song)
        button_before.setObjectName('button_before')

        self.button_play = QPushButton()
        self.button_play.setObjectName('button_play')
        self.button_play.clicked.connect(self.play_pause_song)

        button_next = QPushButton()
        button_next.clicked.connect(self.next_song)
        button_next.setObjectName('button_next')

        self.button_repeat = QPushButton()
        self.button_repeat.clicked.connect(self.toggle_repeat_mode)
        self.button_repeat.setObjectName('button_repeat')

        self.button_random.setFixedSize(40, 40)
        button_before.setFixedSize(40, 40)
        self.button_play.setFixedSize(60, 60)
        button_next.setFixedSize(40, 40)
        self.button_repeat.setFixedSize(40, 40)

        buttons_h_box.addWidget(self.button_random)
        buttons_h_box.addWidget(button_before)
        buttons_h_box.addWidget(self.button_play)
        buttons_h_box.addWidget(button_next)
        buttons_h_box.addWidget(self.button_repeat)

        buttons_container = QWidget()
        buttons_container.setLayout(buttons_h_box)

        main_v_box.addWidget(song_image)
        main_v_box.addWidget(buttons_container)

        self.reproductor_container.setLayout(main_v_box)

    def generate_playlist_user_tab(self):  # Renamed
        main_v_box = QVBoxLayout()

        label_title = QLabel("Mis Playlists")
        label_title.setObjectName(
            "playlist-title-style")  # Add style if needed
        label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # List to display playlists
        self.playlists_list_widget = QListWidget()
        self.playlists_list_widget.setObjectName(
            "playlists-list-style")  # Add style if needed
        # self.playlists_list_widget.itemDoubleClicked.connect(self.load_playlist) # Connect later

        buttons_h_box = QHBoxLayout()

        # --- Buttons ---
        button_load = QPushButton('Cargar')
        button_load.setObjectName('load-style-button')  # Changed name
        button_load.clicked.connect(self.load_selected_playlist)

        # button_modify = QPushButton('Modificar') # Modify functionality not implemented yet
        # button_modify.setObjectName('modify-style-button')
        # # button_modify.clicked.connect(self.modify_selected_playlist)

        button_delete = QPushButton('Eliminar')
        button_delete.setObjectName('delete-style-button')
        button_delete.clicked.connect(self.delete_selected_playlist)

        buttons_h_box.addWidget(button_load)
        # buttons_h_box.addWidget(button_modify)
        buttons_h_box.addWidget(button_delete)

        button_container = QWidget()
        button_container.setLayout(buttons_h_box)

        main_v_box.addWidget(label_title)
        main_v_box.addWidget(self.playlists_list_widget)
        main_v_box.addWidget(button_container)

        self.playlist_saved_user.setLayout(main_v_box)

    def generate_settings_tab(self):
        # Placeholder for future settings
        layout = QVBoxLayout()
        label = QLabel("Ajustes de la aplicación (Próximamente)")
        layout.addWidget(label)
        self.settings_container.setLayout(layout)

    def create_action(self):
        # ... (Actions remain mostly the same) ...
        self.listar_musica_action = QAction(
            'Listar música', self, checkable=True)  # type: ignore
        self.listar_musica_action.setShortcut(QKeySequence("Ctrl+L"))
        self.listar_musica_action.setStatusTip(
            "Aqui puede listar o no la música a reproducir")
        self.listar_musica_action.triggered.connect(self.list_music)
        self.listar_musica_action.setChecked(True)

        self.open_folder_music_action = QAction(
            'Abrir Carpeta', self)  # type: ignore
        self.open_folder_music_action.setShortcut(QKeySequence("Ctrl+O"))
        self.open_folder_music_action.setStatusTip("Abre tu carpeta de música")
        self.open_folder_music_action.triggered.connect(self.open_music)

        self.save_playlist_action = QAction('Guardar Playlist Actual', self)
        self.save_playlist_action.setShortcut(QKeySequence("Ctrl+G"))
        self.save_playlist_action.setStatusTip(
            "Guarda la lista de canciones actual como una nueva playlist")
        self.save_playlist_action.triggered.connect(self.playlist_save)

        self.sign_off_action = QAction('Cerrar sesión', self)
        self.sign_off_action.setShortcut(QKeySequence("Ctrl+W"))
        self.sign_off_action.setStatusTip("Cerrar sesion actual")
        self.sign_off_action.triggered.connect(self.sign_off)

        self.exit_repr_action = QAction('Salir', self)
        self.exit_repr_action.setShortcut(QKeySequence("Ctrl+E"))
        self.exit_repr_action.setStatusTip("Salir del reproductor")
        self.exit_repr_action.triggered.connect(self.exit_repr)

    def create_menu(self):
        # ... (Menu creation remains the same) ...
        self.menuBar()
        menu_file = self.menuBar().addMenu("File")
        menu_file.addAction(self.open_folder_music_action)
        menu_file.addAction(self.save_playlist_action)
        menu_file.addSeparator()
        menu_file.addAction(self.sign_off_action)
        menu_file.addAction(self.exit_repr_action)

        menu_view = self.menuBar().addMenu("View")
        menu_view.addAction(self.listar_musica_action)

    def create_dock(self):
        # ... (Dock creation remains the same) ...
        self.songs_list_panel = QListWidget()
        self.dock = QDockWidget()
        self.dock.setWindowTitle('Lista de canciones')
        self.dock.setFixedWidth(300)
        self.dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea |
            Qt.DockWidgetArea.RightDockWidgetArea
        )
        self.songs_list_panel.itemDoubleClicked.connect(
            self.handle_song_double_click)
        self.dock.setWidget(self.songs_list_panel)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)

    def list_music(self):
        # ... (Show/hide dock remains the same) ...
        if self.listar_musica_action.isChecked():
            self.dock.show()
        else:
            self.dock.hide()

    def open_music(self):
        # ... (Opening music folder remains the same) ...
        initial_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.MusicLocation
        )
        selected_folder = QFileDialog.getExistingDirectory(
            None, "Selecciona una carpeta", initial_dir)

        if selected_folder:  # Only proceed if a folder was selected
            self.current_music_folder = selected_folder
            icon = QIcon('img/music.png')
            self.songs_list_panel.clear()
            self.current_index = -1
            self.song_list = []  # Reset the song list
            try:
                for archivo in os.listdir(self.current_music_folder):
                    ruta_archivo = os.path.join(
                        self.current_music_folder, archivo)
                    # Basic check for mp3 extension
                    if ruta_archivo.lower().endswith(".mp3"):
                        self.song_list.append(ruta_archivo)  # Add full path
                        nombre_archivo, _ = os.path.splitext(archivo)
                        item = QListWidgetItem(nombre_archivo)
                        item.setIcon(icon)
                        # Store full path in item data
                        item.setData(Qt.ItemDataRole.UserRole, ruta_archivo)
                        self.songs_list_panel.addItem(item)
                if not self.song_list:
                    QMessageBox.information(self, "Carpeta Vacía", "La carpeta seleccionada no contiene archivos MP3.", QMessageBox.StandardButton.Ok)
            except Exception as e:
                QMessageBox.critical(self, "Error al Abrir Carpeta",f"No se pudo leer la carpeta: {e}", QMessageBox.StandardButton.Ok)

    def playlist_save(self):
        if not self.current_user_id:
            QMessageBox.warning(self, "Error", "Debe iniciar sesión para guardar playlists.", QMessageBox.StandardButton.Close)
            return
        
        if len(self.song_list) > 0:
            # Pass the user_id and the current song list to the form
            self.form_new_playlist = FormListMusic(
                user_id=self.current_user_id, current_songs=self.song_list)
            # Connect the signal to reload playlists if saved successfully
            self.form_new_playlist.playlist_saved.connect(
                self.load_user_playlists)
            self.form_new_playlist.exec()  # Use exec for modal dialog
        else:
            QMessageBox.warning(
                self, "Lista Vacía", "No hay canciones cargadas para guardar como playlist.", QMessageBox.StandardButton.Close)

    def create_player(self):
        if self.player:
            # Clean up the previous player instance to avoid resource leaks
            self.player.stop()
            self.player.setSource(QUrl())
            self.player.setAudioOutput(None)
            self.player.deleteLater()
            self.player = None
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.player.mediaStatusChanged.connect(self.media_status_changed)
        self.player.errorOccurred.connect(
            self.handle_player_error)  # Add error handling
        self.audioOutput.setVolume(1.0)

    # --- Player Controls & Logic ---
    def media_status_changed(self, status):
        # print('status:', status)
        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            # Only play if intended (prevents auto-play on load)
            if self.playing_reproductor:
                self.player.play()
        elif status == QMediaPlayer.MediaStatus.EndOfMedia:
            if self.is_repeat:
                self.player.setPosition(0)
                self.player.play()
            else:
                self.next_song()

    def handle_player_error(self, error, error_string):
        print(f"Player Error: {error}, {error_string}")
        QMessageBox.critical(self, "Error de Reproducción", f"No se pudo reproducir el archivo: {error_string}")
        # Optionally, try to play the next song or stop playback
        self.playing_reproductor = False
        self.button_play.setStyleSheet("image: url('styles/img/play.png');")

    def play_pause_song(self):
        if not self.player:
            if not self.song_list: # No songs loaded at all
                QMessageBox.warning(self, "Sin Canciones", "Abre una carpeta o carga una playlist.", QMessageBox.StandardButton.Ok)
                return
            else: # Songs are loaded, but player not created yet (first play)
                self.current_index = 0 # Start from the first song
                self.play_song_at_index(self.current_index)
                return # play_song_at_index handles playing state
        
        if self.playing_reproductor:
            self.button_play.setStyleSheet("image: url('styles/img/play.png');")
            self.current_position = self.player.position()
            self.player.pause()
            self.playing_reproductor = False
        else:
            self.button_play.setStyleSheet("image: url('styles/img/stop.png');")
            if self.current_index >= 0: # Resume or play selected
                self.player.setPosition(self.current_position)
                self.player.play()
                self.playing_reproductor = True
            # else: # Should be handled by initial check
            #    self.current_index = 0
            #    self.play_song_at_index(self.current_index)

    def next_song(self):
        if not self.song_list: return # No songs loaded

        if self.is_random:
            self.current_index = random.randint(0, len(self.song_list) - 1)
        else:
            if self.current_index < len(self.song_list) - 1:
                self.current_index += 1
            else:
                self.current_index = 0  # Loop back to the beginning
        self.play_song_at_index(self.current_index)

    def play_previous_song(self):
        if not self.song_list: return # No songs loaded
            
        if self.is_random: # Select a new random song if in random mode
            self.current_index = random.randint(0, len(self.song_list) - 1)
        else:
            if self.current_index > 0:
                self.current_index -= 1
            else:
                self.current_index = len(self.song_list) - 1 # Loop back to the end
        self.play_song_at_index(self.current_index)

    def random_mode_toggle(self):
        self.is_random = not self.is_random
        # Update button style based on state (replace with actual CSS classes/styles)
        if self.is_random:
            self.button_random.setStyleSheet("background-color: rgba(3, 3, 3, 0.8); border: 1px solid #ccc;") # Example active style
        else:
            self.button_random.setStyleSheet("background-color: white; border: 1px solid #aaa;") # Example inactive style
    
    def toggle_repeat_mode(self):
        self.is_repeat = not self.is_repeat
         # Update button style based on state
        if self.is_repeat:
            self.button_repeat.setStyleSheet("background-color: rgba(3, 3, 3, 0.8); border: 1px solid #ccc;") # Example active style
        else:
            self.button_repeat.setStyleSheet("background-color: white; border: 1px solid #aaa;") # Example inactive style

    def handle_song_double_click(self):
        selected_items = self.songs_list_panel.selectedItems()
        if selected_items:
            self.current_index = self.songs_list_panel.row(selected_items[0])
            self.play_song_at_index(self.current_index)
            
    def play_song_at_index(self, index):
        if 0 <= index < len(self.song_list):
            self.current_index = index
            song_path = self.song_list[self.current_index]
            self.create_player() # Ensure player is ready
            source = QUrl.fromLocalFile(song_path)
            
            # Check if the file exists before trying to play
            if not os.path.exists(song_path):
                QMessageBox.warning(self, "Archivo no encontrado", f"El archivo de canción no se encontró:{song_path}")
                # Try playing the next song or stop
                # self.next_song()
                return

            self.player.setSource(source)
            self.current_position = 0 # Start from beginning
            self.playing_reproductor = True
            self.button_play.setStyleSheet("image: url('styles/img/stop.png');")
            # Update the selection in the list widget visually
            self.songs_list_panel.setCurrentRow(self.current_index)
        else:
            print(f"Error: Invalid index {index}")
            # Stop playback if index is invalid
            if self.player: 
                self.player.stop()
            self.playing_reproductor = False
            self.button_play.setStyleSheet("image: url('styles/img/play.png');")
            
    # --- Playlist Management (Biblioteca Tab) --- 
    def load_user_playlists(self):
        if not self.current_user_id:
            # Don't try to load if no user is logged in
            return 
        
        self.playlists_list_widget.clear() # Clear existing list
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT playlist_id, name_playlist FROM playlists WHERE user_id = ? ORDER BY name_playlist", (self.current_user_id,))
            playlists = cursor.fetchall()
            
            icon = QIcon('img/repro2.jpg') # Example icon for playlists
            for playlist in playlists:
                item = QListWidgetItem(playlist["name_playlist"])
                item.setIcon(icon)
                item.setData(Qt.ItemDataRole.UserRole, playlist["playlist_id"]) # Store playlist_id
                self.playlists_list_widget.addItem(item)
                
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error de Base de Datos", f"No se pudieron cargar las playlists: {e}", QMessageBox.StandardButton.Ok)
        finally:
            if conn:
                conn.close()
                
    def load_selected_playlist(self):
        selected_items = self.playlists_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Seleccionar Playlist", "Por favor, selecciona una playlist de la lista para cargarla.", QMessageBox.StandardButton.Ok)
            return
            
        selected_item = selected_items[0]
        playlist_id = selected_item.data(Qt.ItemDataRole.UserRole)
        playlist_name = selected_item.text()
        
        conn = None
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT song_path FROM playlist_songs WHERE playlist_id = ?", (playlist_id,))
            songs = cursor.fetchall()
            if not songs:
                QMessageBox.information(self, "Playlist Vacía", f'La playlist "{playlist_name}" no contiene canciones.', QMessageBox.StandardButton.Ok)
                return
            
            # --- Update the main song list and panel --- 
            self.songs_list_panel.clear()
            self.song_list = []
            self.current_index = -1
            icon = QIcon('img/music.png')
            missing_files = []

            for song in songs:
                song_path = song["song_path"]
                if os.path.exists(song_path): # Check if file still exists
                    self.song_list.append(song_path)
                    nombre_archivo, _ = os.path.splitext(os.path.basename(song_path))
                    item = QListWidgetItem(nombre_archivo)
                    item.setIcon(icon)
                    item.setData(Qt.ItemDataRole.UserRole, song_path) # Store full path
                    self.songs_list_panel.addItem(item)
                else:
                    missing_files.append(song_path)
            
            if missing_files:
                QMessageBox.warning(self, "Archivos Faltantes", f"Algunas canciones de la playlist \"{playlist_name}\" no se encontraron y no fueron cargadas: " + ", ".join(missing_files), QMessageBox.StandardButton.Ok)
                                    
            if self.song_list: # If any songs were loaded successfully
                self.current_index = 0 # Prepare to play the first song
                self.play_song_at_index(self.current_index)
                # Switch focus to the reproducer tab (optional)
                # self.centralWidget().setCurrentIndex(0) 
            else: # No valid songs found in the playlist
                if self.player: self.player.stop()
                self.playing_reproductor = False
                self.button_play.setStyleSheet("image: url('styles/img/play.png');")
                QMessageBox.warning(self, "Error al Cargar", f'No se encontraron archivos válidos en la playlist "{playlist_name}".', QMessageBox.StandardButton.Ok)

        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error de Base de Datos", f"No se pudieron cargar las canciones de la playlist: {e}", QMessageBox.StandardButton.Ok)
        finally:
            if conn:
                conn.close()
    def delete_selected_playlist(self):
        selected_items = self.playlists_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Seleccionar Playlist", "Por favor, selecciona una playlist de la lista para eliminarla.", QMessageBox.StandardButton.Ok)
            return
            
        selected_item = selected_items[0]
        playlist_id = selected_item.data(Qt.ItemDataRole.UserRole)
        playlist_name = selected_item.text()
        
        reply = QMessageBox.question(self, 'Confirmar Eliminación', f'¿Estás seguro de que quieres eliminar la playlist "{playlist_name}"?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            conn = None
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                
                # Delete songs associated with the playlist first (foreign key constraint)
                cursor.execute("DELETE FROM playlist_songs WHERE playlist_id = ?", (playlist_id,))
                # Delete the playlist itself
                cursor.execute("DELETE FROM playlists WHERE playlist_id = ?", (playlist_id,))
                
                conn.commit()
                QMessageBox.information(self, "Playlist Eliminada", f'La playlist "{playlist_name}" ha sido eliminada.', QMessageBox.StandardButton.Ok)
                self.load_user_playlists() # Refresh the list
                
            except sqlite3.Error as e:
                QMessageBox.warning(self, "Error de Base de Datos", f"No se pudo eliminar la playlist: {e}", QMessageBox.StandardButton.Ok)
            finally:
                if conn:
                    conn.close()

    # --- Other Actions --- 
    def sign_off(self):
        # Potentially ask for confirmation
        reply = QMessageBox.question(self, 'Cerrar Sesión', 
                                    '¿Estás seguro de que quieres cerrar sesión?', 
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                    QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.close() # Close the current window
            # Ideally, reopen the login/main menu window here
            # This requires the main application structure to handle window management
            # For now, we just close. The user needs to restart the app to log in again.
            # from main import MainMenu # Avoid circular import if possible
            # self.main_menu_window = MainMenu()
            # self.main_menu_window.show()
    
    def exit_repr(self):
        # Ask for confirmation before exiting
        reply = QMessageBox.question(self, 'Salir', 
                                    '¿Estás seguro de que quieres salir de Sound Fresh?', 
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                    QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.close()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     # You would need a default user_id or handle the case where it's None for testing
#     window = MainWindowRep(user_id=1) # Example: pass a user_id for testing
#     # Initialize the database if running this file directly for testing
#     from src.database.db_setup import initialize_database
#     initialize_database()
#     sys.exit(app.exec())
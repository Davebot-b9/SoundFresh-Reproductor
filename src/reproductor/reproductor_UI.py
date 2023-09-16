import sys
import os
import random
from PyQt6.QtCore import Qt, QStandardPaths, QUrl
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QDockWidget, QStatusBar,
                            QTabWidget, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QFileDialog, QListWidgetItem, QMessageBox)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtGui import QIcon, QPixmap, QAction, QKeySequence
#from reproductor.repr_player import MusicPlayer


class MainWindowRep(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialize_ui()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.current_music_folder = ""
        with open('styles/estilosRep.css', 'r') as file:
            style = file.read()
        self.setStyleSheet(style)
        self.create_player()
        self.playing_reproductor = False
        self.current_index = -1
        self.is_random = False
        

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
        self.settings_container = QWidget()
        tab_bar.addTab(self.reproductor_container,
                    "Reproductor")
        tab_bar.addTab(self.settings_container,
                    "Settings")
        self.generate_repro_tab()
        self.generate_settings_tab()

        tab_h_box = QHBoxLayout()
        tab_h_box.addWidget(tab_bar)

        main_container = QWidget()
        main_container.setLayout(tab_h_box)
        self.setCentralWidget(main_container)

    def generate_repro_tab(self):
        main_v_box = QVBoxLayout()
        buttons_h_box = QHBoxLayout()

        song_image = QLabel()
        pixmap = QPixmap("img/disc.jpg")
        song_image.setPixmap(pixmap)
        song_image.setScaledContents(True)

        button_random = QPushButton()
        button_random.setObjectName('button_random')
        button_before = QPushButton()
        # button_before.clicked.connect(self.play_previous_song)
        button_before.setObjectName('button_before')

        self.button_play = QPushButton()
        self.button_play.setObjectName('button_play')
        self.button_play.clicked.connect(self.play_pause_song)

        button_next = QPushButton()
        #button_next.clicked.connect(self.next_song)
        button_next.setObjectName('button_next')
        
        button_repeat = QPushButton()
        button_repeat.setObjectName('button_repeat')

        button_random.setFixedSize(40, 40)
        button_before.setFixedSize(40, 40)
        self.button_play.setFixedSize(60, 60)
        button_next.setFixedSize(40, 40)
        button_repeat.setFixedSize(40, 40)

        buttons_h_box.addWidget(button_random)
        buttons_h_box.addWidget(button_before)
        buttons_h_box.addWidget(self.button_play)
        buttons_h_box.addWidget(button_next)
        buttons_h_box.addWidget(button_repeat)

        buttons_container = QWidget()
        buttons_container.setLayout(buttons_h_box)

        main_v_box.addWidget(song_image)
        main_v_box.addWidget(buttons_container)

        self.reproductor_container.setLayout(main_v_box)

    def generate_settings_tab(self):
        pass

    def create_action(self):
        self.listar_musica_action = QAction(
            'Listar música', self, checkable=True)  # type: ignore
        self.listar_musica_action.setShortcut(QKeySequence("Ctrl+L"))
        self.listar_musica_action.setStatusTip(
            "Aqui puede listar o no la música a reproducir")
        # signal
        self.listar_musica_action.triggered.connect(self.list_music)
        self.listar_musica_action.setChecked(True)

        self.open_folder_music_action = QAction(
            'Abrir Carpeta', self)  # type: ignore
        self.open_folder_music_action.setShortcut(QKeySequence("Ctrl+O"))
        self.open_folder_music_action.setStatusTip("Abre tu carpeta de música")
        # signal
        self.open_folder_music_action.triggered.connect(self.open_music)

    def create_menu(self):
        self.menuBar()
        menu_file = self.menuBar().addMenu("File")
        menu_file.addAction(self.open_folder_music_action)

        menu_view = self.menuBar().addMenu("View")
        menu_view.addAction(self.listar_musica_action)

    def create_dock(self):
        self.songs_list = QListWidget()
        self.dock = QDockWidget()
        self.dock.setWindowTitle('Lista de canciones')
        self.dock.setFixedWidth(300)
        self.dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea |
            Qt.DockWidgetArea.RightDockWidgetArea
        )
        self.songs_list.itemSelectionChanged.connect(
            self.play_pause_song)
        self.dock.setWidget(self.songs_list)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)

    def list_music(self):
        if self.listar_musica_action.isChecked():
            self.dock.show()
        else:
            self.dock.hide()

    def open_music(self):
        initial_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.MusicLocation
        )
        self.current_music_folder = QFileDialog.getExistingDirectory(
            None, "Selecciona una carpeta", initial_dir)
        icon = QIcon('img/music.png')
        self.songs_list.clear()
        self.current_index = -1
        for archivo in os.listdir(self.current_music_folder):
            ruta_archivo = os.path.join(self.current_music_folder, archivo)
            if ruta_archivo.endswith(".mp3"):
                nombre_archivo, _ = os.path.splitext(
                    archivo)  # Dividir nombre y extensión
                # Agregar solo el nombre
                item = QListWidgetItem(nombre_archivo)
                item.setIcon(icon)
                self.songs_list.addItem(item)

    def create_player(self):
        # if self.player:
        #     self.player.deleteLater()
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.player.mediaStatusChanged.connect(self.media_status_changed)
        self.audioOutput.setVolume(1.0)

    def play_pause_song(self):
        if self.player.mediaStatus() == QMediaPlayer.MediaStatus.LoadedMedia:
            if self.playing_reproductor:
                self.player.pause()
                self.playing_reproductor = False
            else:
                self.player.play()
                self.playing_reproductor = True
        else:
            selected_item = self.songs_list.currentItem()
            if selected_item:
                song_name = selected_item.text() + ".mp3"
                song_folder_path = os.path.join(
                    self.current_music_folder, song_name)
                source = QUrl.fromLocalFile(song_folder_path)
                self.player.setSource(source)

    def media_status_changed(self, status):
        print('status:', status)
        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            self.player.play()
        # elif status == QMediaPlayer.MediaStatus.BufferedMedia:
        #     if not self.playing_reproductor:
        #         self.player.pause()

    # def next_song(self):
    #     if self.current_index < self.songs_list.count() - 1:
    #         self.current_index += 1
            # self.handle_song_selection()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindowRep()
    sys.exit(app.exec())

# import os
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QObject, QUrl
#from src.reproductor.reproductor_UI import MainWindowRep

class MusicPlayer(QObject):
    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()  # Creamos el reproductor aquí
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.player.mediaStatusChanged.connect(self.media_status_changed)
        self.audioOutput.setVolume(1.0)
        self.playing_reproductor = False
        self.current_index = -1
        self.is_random = False

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
                self.player.setMedia(source)

    def media_status_changed(self, status):
        print('status:', status)
        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            if self.playing_reproductor:
                self.player.play()
        elif status == QMediaPlayer.MediaStatus.BufferedMedia:
            if not self.playing_reproductor:
                self.player.pause()

import typing
import sys
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QLabel, QMessageBox, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QPixmap, QIcon

class MainWindowP(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,500,500)
        self.setMaximumSize(500,500)
        self.setWindowTitle('Sound Fresh')
        self.setWindowIcon(QIcon('icon.png'))
        self.generate_content()
    
    def generate_content(self):
        image_path = 'img\\dino.jpg'
        try:
            with open(image_path):
                image_label = QLabel(self)
                image_label.setPixmap(QPixmap(image_path))
        except FileNotFoundError as e:
            QMessageBox.warning(self, "Error Image",
            f'Image not found: {e}',
            QMessageBox.StandardButton.Close,
            QMessageBox.StandardButton.Close)
        except Exception as e:
            QMessageBox.warning(self, "Error Main view",
            f'Error in the main view: {e}',
            QMessageBox.StandardButton.Close,
            QMessageBox.StandardButton.Close)

if __name__ == '__main__':
    app = QApplication(sys.argv) # type: ignore
    main_menu = MainWindowP()
    sys.exit(app.exec())
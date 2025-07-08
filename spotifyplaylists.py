import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget,QPushButton, QVBoxLayout, QMessageBox, QLineEdit
from PyQt5.QtCore import QDir, QSize
from PyQt5.QtGui import QIcon

class playlistinstaller(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Playlist Installer")
        self.setGeometry(100, 100, 300, 200)
        self.setMinimumSize(300, 200)
        self.layout = QVBoxLayout()
        self.install_button = QPushButton("Install Playlist")
        self.install_button.clicked.connect(self.install_playlist)
        self.lineEdit = QLineEdit(self)
        self.layout.addWidget(self.lineEdit)
        self.lineEdit.setPlaceholderText("Enter playlist name...")
        self.install_button.clicked.connect(lambda: self.install_playlist(self.lineEdit.text()))
        self.layout.addWidget(self.install_button)
        self.setLayout(self.layout)
    def install_playlist(self, userinput):
        subprocess.check_call([sys.executable, 'spotdl', 'download', userinput])
        self.lineEdit.clear()
        QMessageBox.information(self, "Success", f"Playlist '{userinput}' installed successfully!")
        sys.exit(0)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    installer = playlistinstaller()
    installer.show()
    sys.exit(app.exec_())

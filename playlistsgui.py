import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QMessageBox
from PyQt5.QtCore import QDir, QSize
from PyQt5.QtGui import QIcon

class FileChooser(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Playlist Chooser")
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumSize(600, 400)
        self.filetree = QTreeWidget()
        self.filetree.setStyleSheet("""
            QTreeView { background-color: #A996EB; color: white; }
            QTreeView::item { padding: 5px; }
            QTreeView::item:hover { background-color: #D1C4E9; }
        """)
        icon_path = "C:/Users/grish/csfolders/mp3player/Assets/folder!.png"  # Default icon path
        if not os.path.exists(icon_path):
            print(f"No icon found at {icon_path}. Using default icon.")
            icon_path = ":/default/folder"
        self.icon = QIcon(icon_path)
        self.filetree.setHeaderLabels(["Playlists"])
        self.filetree.itemDoubleClicked.connect(self.folderselector)
        default_path = "C:/Users/grish/csfolders/mp3player/playlists"
        self.populate_tree(default_path)
        self.filetree.setIconSize(QSize(24, 24))
        layout = QVBoxLayout()
        layout.addWidget(self.filetree)
        self.setLayout(layout)
        self.selected_folder = None

    def populate_tree(self, folderpath):
        self.filetree.clear()
        if not os.path.exists(folderpath):
            QMessageBox.critical(self, "Error", f"No path found: {folderpath}")
            return
        folderitem = QTreeWidgetItem(self.filetree)
        folderitem.setText(0, os.path.basename(folderpath))
        folderitem.setIcon(0, self.icon)
        folderitem.setData(0, 1, folderpath)
        self.song_populator(folderitem, folderpath)

    def song_populator(self, parent_item, folderpath):
        folderdir = QDir(folderpath)
        folderdir.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)
        for entry in folderdir.entryList():
            entry_path = os.path.join(folderpath, entry)
            item = QTreeWidgetItem(parent_item)
            item.setText(0, entry)
            if os.path.isdir(entry):
                item.setIcon(0, self.icon)
                item.setData(0, 1, entry_path)
            else:
                item.setIcon(0, self.icon)
                item.setData(0, 1, entry_path)

    def folderselector(self, item, column):
        chosen_folder = item.data(0, 1)
        if os.path.isdir(chosen_folder):
            self.selected_folder = chosen_folder
            print(chosen_folder)
            sys.exit(0)
        else:
            QMessageBox.warning(self, "Invalid Selection", "You probably selected a file. Use a folder!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    chooser = FileChooser()
    chooser.show()
    sys.exit(app.exec_())

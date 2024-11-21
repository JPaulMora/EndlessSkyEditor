import os
import platform
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from save_viewer import SaveViewer


class EndlessEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Endless Sky Save File Editor")
        self.setGeometry(100, 100, 600, 400)

        # Layout
        self.layout = QVBoxLayout(self)

        # File browser for the game installation folder
        game_folder_layout = QHBoxLayout()
        self.game_folder_input = QLineEdit()
        self.game_folder_input.setPlaceholderText("Select the game installation folder...")
        self.game_folder_browse_button = QPushButton("Browse")
        self.game_folder_browse_button.clicked.connect(self.browse_game_folder)
        game_folder_layout.addWidget(self.game_folder_input)
        game_folder_layout.addWidget(self.game_folder_browse_button)
        self.layout.addLayout(game_folder_layout)

        # File browser for the save folder
        save_folder_layout = QHBoxLayout()
        self.save_folder_input = QLineEdit()
        self.save_folder_input.setText(self.get_default_save_path())
        self.save_folder_input.setPlaceholderText("Select the save folder...")
        self.save_folder_browse_button = QPushButton("Browse")
        self.save_folder_browse_button.clicked.connect(self.browse_save_folder)
        save_folder_layout.addWidget(self.save_folder_input)
        save_folder_layout.addWidget(self.save_folder_browse_button)
        self.layout.addLayout(save_folder_layout)

        # Save list
        self.save_list = QListWidget()
        self.layout.addWidget(self.save_list)

        # Load saves
        self.load_button = QPushButton("Load Save")
        self.load_button.clicked.connect(self.load_selected_save)
        self.layout.addWidget(self.load_button)

        # Load the initial save files
        self.load_saves()


    def get_default_save_path(self):
        """Return the default save path for Endless Sky based on the operating system."""
        system = platform.system()
        if system == "Windows":
            return os.path.join(os.getenv("APPDATA"), "endless-sky", "saves")
        elif system == "Linux":
            return os.path.expanduser("~/.local/share/endless-sky/saves")
        elif system == "Darwin":  # macOS
            return os.path.expanduser("~/Library/Application Support/endless-sky/saves")
        else:
            return ""
        

    def browse_game_folder(self):
        """Browse and set the game installation folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Game Installation Folder")
        if folder:
            self.game_folder_input.setText(folder)

    def browse_save_folder(self):
        """Browse and set the save folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Save Folder")
        if folder:
            self.save_folder_input.setText(folder)
            self.load_saves()  # Reload saves when the folder changes

    def load_saves(self):
        """Load save files into the list."""
        self.save_list.clear()
        save_folder = self.save_folder_input.text()
        if os.path.isdir(save_folder):
            try:
                save_files = [file for file in os.listdir(save_folder) if file.endswith('.txt')]
                self.save_list.addItems(save_files)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load save files: {e}")
        else:
            QMessageBox.critical(self, "Error", "Save folder is invalid or does not exist!")

    def load_selected_save(self):
        """Load the selected save file and display its content."""
        selected_items = self.save_list.selectedItems()
        if selected_items:
            save_file = os.path.join(self.save_folder_input.text(), selected_items[0].text())
            self.open_ship_viewer(save_file)
        else:
            QMessageBox.warning(self, "Warning", "No save file selected!")

    def open_ship_viewer(self, file_path):
        """Open the SaveViewer module."""
        self.ship_viewer = SaveViewer(file_path)
        self.ship_viewer.show()


if __name__ == "__main__":
    app = QApplication([])
    editor = EndlessEditor()
    editor.show()
    app.exec()

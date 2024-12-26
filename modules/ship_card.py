from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QSizePolicy,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class ShipCard(QWidget):
    def __init__(self, image_path, title, model, description2, parent=None):
        super().__init__(parent)

        # Create the main horizontal layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(20)

        # Image
        self.image_label = QLabel()
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print("pixmap is null", image_path)

            # Placeholder pixmap if image not found
            pixmap = QPixmap(100, 100)
            pixmap.fill(Qt.gray)
        else:
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap)
        self.image_label.setFixedSize(100, 100)
        self.image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Title and descriptions
        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)

        if title is None:
            title = "- No name -"

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        self.desc1_label = QLabel(model)
        self.desc1_label.setStyleSheet("color: gray; font-size: 12px;")

        self.desc2_label = QLabel(description2)
        self.desc2_label.setStyleSheet("color: gray; font-size: 12px;")

        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.desc1_label)
        text_layout.addWidget(self.desc2_label)
        text_layout.addStretch()  # Pushes the descriptions up

        # Edit Button
        self.edit_button = QPushButton("Edit")

        # Add widgets to the main layout
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(text_layout)
        main_layout.addStretch()  # Pushes the button to the right
        main_layout.addWidget(self.edit_button)

        self.setLayout(main_layout)
        self.setFixedHeight(120)  # Fixed height for uniformity

        # Optionally, connect the edit button to a slot
        self.edit_button.clicked.connect(self.on_edit_clicked)

    def on_edit_clicked(self):
        # Placeholder for edit button functionality
        print(f"Edit button clicked for: {self.title_label.text()}")

import re
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QScrollArea, QHBoxLayout, QGroupBox, QGridLayout
)
from PySide6.QtCore import Qt


class SaveViewer(QWidget):
    def __init__(self, file_path):
        super().__init__()
        self.setWindowTitle("Save Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.file_path = file_path

        # Main layout
        self.main_layout = QVBoxLayout(self)

        # File path label
        self.file_label = QLabel(f"Editing: {file_path}")
        self.file_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.file_label)

        # Scrollable area for the form
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        self.form_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(scroll_area)

        # Add the Pilot Data GroupBox
        self.pilot_box = QGroupBox("Pilot Data")
        self.form_layout.addWidget(self.pilot_box)

        # Add a checkbox for controlling the reputation section visibility
        self.reputation_checkbox = QPushButton("Reputation (Click to Expand/Collapse)")
        self.reputation_checkbox.setCheckable(True)
        self.reputation_checkbox.setChecked(True)
        self.reputation_checkbox.clicked.connect(self.toggle_reputation_section)
        self.form_layout.addWidget(self.reputation_checkbox)

        # Add the actual reputation section (QGroupBox)
        self.reputation_section = QGroupBox()
        self.reputation_section_layout = QGridLayout()
        self.reputation_section.setLayout(self.reputation_section_layout)
        self.form_layout.addWidget(self.reputation_section)

        # Save button
        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_changes)
        self.main_layout.addWidget(self.save_button)

        # Editable fields dictionary
        self.fields = {}

        # Load and parse the file
        self.load_file()


    def toggle_reputation_section(self):
        """Show or hide the reputation section based on the checkbox state."""
        is_visible = self.reputation_checkbox.isChecked()
        self.reputation_section.setVisible(is_visible)


    def load_file(self):
        """Load and parse the file to populate editable fields."""
        try:
            with open(self.file_path, "r") as file:
                content = file.readlines()

            self.parse_pilot_data(content)
            self.parse_reputation(content)
        except FileNotFoundError:
            self.form_layout.addWidget(QLabel("Error: File not found."))

    def parse_pilot_data(self, lines):
        """Parse the pilot, date, system, and planet."""
        # Create a non-toggleable box for pilot data
        pilot_layout = QFormLayout()
        self.pilot_box.setLayout(pilot_layout)

        # Parse Pilot
        pilot_line = lines[0].strip()
        if pilot_line.startswith("pilot"):
            pilot_name = pilot_line.split(" ", 1)[1]
            self.fields["pilot"] = QLineEdit(pilot_name)
            pilot_layout.addRow("Pilot Name:", self.fields["pilot"])

        # Parse Date
        date_line = lines[1].strip()
        if date_line.startswith("date"):
            date_value = date_line.split(" ", 1)[1]
            self.fields["date"] = QLineEdit(date_value)
            pilot_layout.addRow("Date:", self.fields["date"])

        # Parse System and Planet
        system = next((line.split(" ", 1)[1].strip() for line in lines if line.startswith("system")), None)
        planet = next(
            (line.split(" ", 1)[1].strip().strip('"') for line in lines if line.startswith("planet")), None
        )

        if system:
            self.fields["system"] = QLineEdit(system)
            pilot_layout.addRow("System:", self.fields["system"])
        if planet:
            self.fields["planet"] = QLineEdit(planet)
            pilot_layout.addRow("Planet:", self.fields["planet"])


    def parse_reputation(self, lines):
        """Parse the reputation section."""
        start_index = next((i for i, line in enumerate(lines) if line.strip() == '"reputation with"'), None)
        if start_index is not None:
            index = start_index + 1
            row = 0  # Track rows in the collapsible layout
            while index < len(lines):
                line = lines[index]
                if line.startswith("\t"):
                    match = re.match(r'\s*"?([^"]+)"?\s+(-?\d+)', line.strip())
                    if match:
                        faction, reputation = match.groups()
                        faction_field = QLineEdit(faction.strip())
                        reputation_field = QLineEdit(reputation.strip())

                        # Store fields for saving
                        self.fields[f"faction_{index}"] = faction_field
                        self.fields[f"reputation_{index}"] = reputation_field

                        # Add to collapsible layout
                        self.reputation_section_layout.addWidget(faction_field, row, 0)
                        self.reputation_section_layout.addWidget(reputation_field, row, 1)
                        row += 1
                else:
                    break
                index += 1

    def save_changes(self):
        """Save changes back to the file."""
        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()

            # Update pilot and date
            lines[0] = f"pilot {self.fields['pilot'].text()}\n"
            lines[1] = f"date {self.fields['date'].text()}\n"

            # Update system and planet
            for i, line in enumerate(lines):
                if line.startswith("system"):
                    lines[i] = f'system {self.fields["system"].text()}\n'
                elif line.startswith("planet"):
                    lines[i] = f'planet "{self.fields["planet"].text()}"\n'

            # Update reputation
            start_index = next((i for i, line in enumerate(lines) if line.strip() == '"reputation with"'), None)
            if start_index is not None:
                index = start_index + 1
                while index < len(lines):
                    line = lines[index]
                    if line.startswith("\t"):
                        faction_field = self.fields.get(f"faction_{index}")
                        reputation_field = self.fields.get(f"reputation_{index}")
                        if faction_field and reputation_field:
                            lines[index] = f'\t"{faction_field.text()}" {reputation_field.text()}\n'
                    else:
                        break
                    index += 1

            # Write back to the file
            with open(self.file_path, "w") as file:
                file.writelines(lines)

            QMessageBox.information(self, "Success", "Changes saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save changes: {e}")


if __name__ == "__main__":
    app = QApplication([])
    viewer = ShipViewer("path/to/your/savefile.txt")
    viewer.show()
    app.exec()
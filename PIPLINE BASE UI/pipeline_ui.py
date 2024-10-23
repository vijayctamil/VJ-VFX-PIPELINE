import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

# Function to create the project directory structure
def create_project_structure(project_name):
    base_path = os.path.join(os.getcwd(), project_name)  # Creates the project structure in the current working directory

    directories = [
        "Assets/Characters",
        "Assets/Environments",
        "Shots/Shot01/Animation",
        "Shots/Shot01/FX",
        "Shots/Shot01/Render",
        "Compositing/Shot01",
        "Cache/Shot01",
        "Scripts",
        "Reference",
        "Deliverables"
    ]

    try:
        for directory in directories:
            path = os.path.join(base_path, directory)
            os.makedirs(path, exist_ok=True)
        return True, base_path
    except Exception as e:
        return False, str(e)

# Main UI window class
class PipelineApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        # Window properties
        self.setWindowTitle('VFX Pipeline Folder Creator')
        self.setGeometry(100, 100, 400, 200)

        # Label and input for project name
        self.label = QLabel('Enter Project Name:', self)
        self.project_name_input = QLineEdit(self)

        # Create button
        self.create_button = QPushButton('Create Project Structure', self)
        self.create_button.clicked.connect(self.on_create_button_click)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.project_name_input)
        layout.addWidget(self.create_button)

        self.setLayout(layout)

    def on_create_button_click(self):
        # Get the project name from the input
        project_name = self.project_name_input.text()

        if not project_name:
            self.show_message_box("Error", "Please enter a valid project name!")
            return

        # Call the function to create the directory structure
        success, message = create_project_structure(project_name)

        if success:
            self.show_message_box("Success", f"Project structure created successfully at:\n{message}")
        else:
            self.show_message_box("Error", f"Failed to create project structure:\n{message}")

    def show_message_box(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

# Main program
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PipelineApp()
    window.show()
    sys.exit(app.exec_())

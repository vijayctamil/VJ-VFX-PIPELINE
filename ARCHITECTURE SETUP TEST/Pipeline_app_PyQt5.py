# Install dependencies: PyQt5, requests
import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QLineEdit, QFileDialog

class PipelineApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pipeline Manager")

        # Layout
        layout = QVBoxLayout()

        # Label to display messages
        self.label = QLabel("Projects will appear here")

        # Text boxes to enter project name and status
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter project name")
        
        self.status_input = QLineEdit()
        self.status_input.setPlaceholderText("Enter project status")
        
        # Button to post project data
        self.post_button = QPushButton("Post Project")

        # Button to fetch projects
        self.fetch_button = QPushButton("Fetch Projects")

        # Button to open file dialog
        self.browse_button = QPushButton("Browse File")

        # Button to upload the file
        self.upload_button = QPushButton("Upload Files")

        # Add widgets to layout
        layout.addWidget(self.label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.status_input)
        layout.addWidget(self.post_button)
        layout.addWidget(self.fetch_button)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.upload_button)

        # Set the layout to the central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connect button click to fetching projects
        self.fetch_button.clicked.connect(self.fetch_projects)
        self.post_button.clicked.connect(self.post_projects)
        self.browse_button.clicked.connect(self.browse_file)
        self.upload_button.clicked.connect(self.upload_file)

        #Variable to store the selected file path
        self.selected_file = None

    # Function to fetch projects from Flask server
    def fetch_projects(self):
        response = requests.get("http://localhost:5000/projects")
        if response.status_code == 200:
            projects = response.json()
            self.label.setText(f"Projects: {projects}")
        else:
            self.label.setText("Failed to fetch projects")

    # Function to post projects from Flask server
    def post_projects(self):
        # Get data from input fields
        project_name = self.name_input.text()
        project_status = self.status_input.text()

        # Prepare data for the POST request
        data = {
            "name" : project_name,
            "status" : project_status
        }

        # Send POST request to Flask server

        response = requests.post("http://localhost:5000/projects", json=data)

        if response.status_code == 201:
            result = response.json()
            self.label.setText(f"Response: {result}")
        else:
            self.label.setText(f"Failed to create project. Status Code: {response.status_code}")


    # Function to open file dialog and select file
    def browse_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Upload", "", "All Files (*);;Text Files (*.txt)", options=options)
        
        if file_path:
            self.selected_file = file_path
            self.label.setText(f"Selected File: {file_path}")
        else:
            self.label.setText("No file selected")

    def upload_file(self):
        if(self.selected_file):
            # Prepare the file for uploading
            file_data = {'file': open(self.selected_file, 'rb')}

            # Send POST request to Flask server to upload file
            response = requests.post("http://localhost:5000/upload", files=file_data)

            if(response.status_code == 202):
                result = response.json()
                self.label.setText(f"Upload Response : {result}")
            else:
                self.label.setText(f"Failed to upload file. Status Code : {response.status_code}")
        else:
            self.label.setText(f"No file selected for upload")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PipelineApp()
    window.show()
    sys.exit(app.exec_())

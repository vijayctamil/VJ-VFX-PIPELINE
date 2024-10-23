# test_flask_app.py
import sys
sys.path.append("C:/Users/ADMIN/Desktop/VJ VFX PIPELINE/ARCHITECTURE SETUP TEST/")
import pytest
from flask import Flask
from flask_app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test retrieving projects
def test_get_projects(client):
    response = client.get('/projects')
    assert response.status_code == 200

# Test project creation
def test_create_project(client):
    project_data = {'name': 'Test Project', 'status': 'in-progress'}
    response = client.post('/projects', json=project_data)
    assert response.status_code == 201

# Test file upload
def test_file_upload(client):
    data = {'file': (open('test_file.txt', 'rb'), 'aaa.txt')}
    response = client.post('/upload', data=data)
    assert response.status_code == 201

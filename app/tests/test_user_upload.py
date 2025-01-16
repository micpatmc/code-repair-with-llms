import pytest
import shutil
from fastapi.testclient import TestClient
from pathlib import Path
from app.main import app

client = TestClient(app)

UPLOAD_DIR = Path("./uploads")

API = "/api/user-upload"

@pytest.fixture(scope="function", autouse=True)
def clean_upload_dir():

    if UPLOAD_DIR.exists():
        shutil.rmtree(UPLOAD_DIR)
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    yield


def test_no_files_uploaded():
    """
        Test for when api is called but no files are uploaded
    """
    
    response = client.post(API, files=[])

    assert response.status_code == 400
    assert response.json()["detail"] == "No files uploaded."


def test_single_file_uploaded():
    '''
        Test uploading a single non-zipped file
    '''

    content = "Test file content"

    response = client.post(
        API,
        files={"files": ("test.txt", content, "text/plain")},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "File uploaded successfully"
    
    # Construct the file path using the returned folder ID (`fid`)
    uploaded_file_path = UPLOAD_DIR / response.json()["session_id"] / "test.txt"

    # Assert that the file exists in the expected location
    assert uploaded_file_path.exists(), f"File was not uploaded at {uploaded_file_path}"


def test_multiple_files_uploaded():
    '''
        Test uploading multiple files not including any zips
    '''

    files = [
        ("files", (f"test_file_{i}.txt", f"Test file {i} content", "text/plain"))
        for i in range(100)
    ]

    response = client.post(
        API,
        files=files,
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Folder uploaded successfully."


def test_zip_with_single_file_uploaded():
    '''
        Test uploading a zip file with one file
    '''


def test_zip_with_multiple_files_uploaded():
    '''
        Test uploading a zip file with many files
    '''


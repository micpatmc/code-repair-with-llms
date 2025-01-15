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
    print(response)
    assert response.status_code == 400
    assert response.json()["detail"] == "No files uploaded."


def test_single_file_upload():
    '''
        Test uploading a single non-zipped file
    '''

    content = "Test file content"

    response = client.post(
        API,
        files={"files": ("test.txt", content, "text/plain")},
    )

    print(response)
    assert response.status_code == 200
    assert response.json()["message"] == "File uploaded successfully"
    
    # Construct the file path using the returned folder ID (`fid`)
    uploaded_file_path = UPLOAD_DIR / response.json()["fid"] / "test.txt"

    # Assert that the file exists in the expected location
    assert uploaded_file_path.exists(), f"File was not uploaded at {uploaded_file_path}"


            

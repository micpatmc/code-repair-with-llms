import pytest
import shutil
import zipfile
import io
from fastapi.testclient import TestClient
from pathlib import Path
from main import app

client = TestClient(app)

UPLOAD_DIR = Path("./uploads")

# Binary representation of steps: 1, 3, 5
pipeline_steps = 21

API = f"/api/initiate_pipeline?pipeline_steps={pipeline_steps}"

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
        headers={
            "accept": "application/json",
        },
    )

    print(f"Response to single file upload test: {response}")

    assert response.status_code == 200
    assert response.json()["message"] == "File uploaded successfully."
    
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
    # Create the content of the single file to be zipped
    file_content = b"This is the content of the single file."

    # Create an in-memory buffer for the ZIP file
    zip_buffer = io.BytesIO()

    # Create a ZIP file in memory with the single file
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr('single_file.txt', file_content)

    # Get the contents of the in-memory ZIP file
    zip_file_data = zip_buffer.getvalue()

    # Prepare data for the API call 
    zip_file = {"files": ("test.zip", zip_file_data, "application/zip")} 

    response = client.post(API,  files=zip_file)

    # Assert successful upload (status code 200)
    assert response.status_code == 200
    assert response.json()["message"] == "Zip File uploaded and extracted successfully"
    assert len(response.json()["files"]) > 0



def test_zip_with_multiple_files_uploaded():
    '''
        Test uploading a zip file with many files
    '''

    files = [
        ("files", (f"test_zipfile_{i}.txt", f"Test file {i} content"))
        for i in range(100)
    ]

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for file_name, file_content in files:
            file_name = file_content[0]
            content_to_write = file_content[1] # Access the second element (content)
            zip_file.writestr(file_name, content_to_write.encode())

    zip_file_data = zip_buffer.getvalue()

    zip_file = {"files": ("test.zip", zip_file_data, "application/zip")} 

    response = client.post(API,  files=zip_file)

    # Assert successful upload (status code 200)
    assert response.status_code == 200
    assert response.json()["message"] == "Zip File uploaded and extracted successfully"
    assert len(response.json()["files"]) > 0


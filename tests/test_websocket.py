import pytest
import bson
from fastapi.testclient import TestClient
from main import app

# Create the TestClient instance once for all tests
client = TestClient(app)

# Binary representation of steps: 1, 3, 5
pipeline_steps = 21

API = f"/api/initiate_pipeline?pipeline_steps={pipeline_steps}"
session_id: str = None

def test_single_file_uploaded():
    '''
        Test uploading a single non-zipped file
    '''

    global session_id
    content = "Test file content"

    response = client.post(
        API,
        files={"files": ("test.txt", content, "text/plain")},
        headers={
            "accept": "application/json",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "File uploaded successfully."

    session_id = response.json()["session_id"]


@pytest.mark.asyncio
async def test_websocket_connection():
    """Test a WebSocket connection and message exchange."""

    global session_id
    assert session_id is not None

    with client.websocket_connect(f"/start-llm-session?websocket=true&session_id={session_id}") as websocket:       
        
        # Test initial connection
        message = bson.BSON.encode({"action": "TEXT_MESSAGE", "type": "message", "content": "Hello Server"})
        websocket.send_bytes(message)

        response_data = websocket.receive_bytes()
        response = bson.BSON(response_data).decode()

        assert response["type"] == "message"
        assert response["content"] == "Server received: Hello Server"


@pytest.mark.asyncio
async def test_websocket_file_transfer():
    global session_id
    assert session_id is not None

    with client.websocket_connect(f"/start-llm-session?websocket=true&session_id={session_id}") as websocket: 
        
        request = bson.encode({"action": "READY_FOR_FILE"})
        websocket.send_bytes(request)

        # Expect START_FILE_TRANSFER message
        response_data = websocket.receive_bytes()
        response = bson.decode(response_data)

        print(response)

        assert response["type"] == "message"
        assert "content" in response
        
        # # Validate the received file (assuming it's a text file for now)
        # assert file_content.decode() == "Test file content"

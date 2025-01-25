import pytest
from fastapi.testclient import TestClient
from main import app

# Create the TestClient instance once for all tests
client = TestClient(app)

API = "/api/user-upload"

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

    # Use the context manager for WebSocketTestSession
    with client.websocket_connect(f"/start-llm-session?websocket=true&session_id={session_id}") as websocket:       
        
        # Test initial connection
        websocket.send_text("Hello Server")
        response = websocket.receive_text()
        assert response == "Message from the server: received the following: Hello Server"

        # Test sending and receiving another message
        websocket.send_text("Test Message")
        response = websocket.receive_text()
        assert response == "Message from the server: received the following: Test Message"



# async def test_faulty_websocket_connection():

#     assert()

import pytest
from fastapi.testclient import TestClient
from main import app

# Create the TestClient instance once for all tests
client = TestClient(app)


@pytest.mark.asyncio
async def test_websocket_connection():
    """Test a WebSocket connection and message exchange."""
    # Use the context manager for WebSocketTestSession
    with client.websocket_connect("/start-llm-session?websocket=true") as websocket:
       
        session_response = websocket.receive_json()
        assert "session" in session_response

        session_id = session_response["session_id"]
        assert isinstance(session_id, str) and len(session_id) > 0

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

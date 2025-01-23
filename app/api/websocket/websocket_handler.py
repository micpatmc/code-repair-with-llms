from fastapi import WebSocket, WebSocketDisconnect
from app.utils.zip_handler import upload_zip
from app.utils.file_handler import upload_file
from app.utils.folder_handler import upload_folder
from app.api.websocket.websocket_connection_manager import WebSocketConnectionManager
from app.core.session_manager import SessionManager

class WebSocketHandler:
    '''
        Handles individual websockets
    '''


    def __init__(self, session_manager: SessionManager):
        self.connection_manager = WebSocketConnectionManager()
        self.session_manager = session_manager
        self.CONNECTED = True

    async def handle_connection(self, websocket: WebSocket):

        # without relying on query_params directly
        await websocket.accept()
        session_id = None

        try:
        
            # While connected to 
            while self.CONNECTED:

                session_id = websocket.query_params.get("session_id")
                self.check_session_id(websocket, session_id)

                data = await websocket.receive_text()

                print(f"Received message from Client: {data}:")

                await websocket.send_text(f"Message from the server: received the following: {data}")

        except WebSocketDisconnect:
            self.connection_manager.disconnect(websocket)
            print("Client disconnected")


    async def check_session_id(self, websocket: WebSocket, session_id: str) -> bool:
          
            if not session_id:
                await websocket.close(code=4001, reason="Session ID is missing")
                return
            
            if not self.session_manager.validate_session(session_id):
                await websocket.close(code=4002, reason="Invalid or expired session ID")
                return
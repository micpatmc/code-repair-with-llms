from fastapi import WebSocket, WebSocketDisconnect
from app.api.rest.utils.zip_handler import upload_zip
from app.api.rest.utils.file_handler import upload_file
from app.api.rest.utils.folder_handler import upload_folder
from app.api.websocket_connection_manager import WebSocketConnectionManager
from app.api.session_manager import SessionManager

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

        session_id = self.session_manager.create_session()
        await websocket.send_text(session_id)

        await self.connection_manager.connect(websocket, session_id)

        try:

            # While connected to 
            while self.CONNECTED:
                data = await websocket.receive_text()

                print(f"Received message from Client: {data}:")

                await websocket.send_text(f"Message from the server: received the following: {data}")

        except WebSocketDisconnect:
            self.connection_manager.disconnect(websocket)
            print("Client disconnected")

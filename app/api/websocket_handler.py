from fastapi import WebSocket, WebSocketDisconnect
from app.api.utils.zip_handler import upload_zip
from app.api.utils.file_handler import upload_file
from app.api.utils.folder_handler import upload_folder
from app.api.websocket_connection_manager import WebSocketConnectionManager


class WebSocketHandler:
    '''
        Handles individual websockets
    '''

    def __init__(self):
        self.connection_manager = WebSocketConnectionManager()
        self.CONNECTED = True

    async def handle_connection(self, websocket: WebSocket):
        
        print(f"WebSocket type: {type(websocket)}")

        # Just for testing purposes, you can use a mock parameter check
        # without relying on query_params directly
        await self.connection_manager.connect(websocket)

        try:

            # While connected to 
            while CONNECTED:
                data = await websocket.receive_text()

                print(f"Received message from Client: {data}:")

                await websocket.send_text(f"Message from the server: received the following: {data}")

        except WebSocketDisconnect:
            self.connection_manager.disconnect(websocket)
            print("Client disconnected")

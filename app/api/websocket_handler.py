from fastapi import WebSocket, WebSocketDisconnect
from app.api.utils.socket_connection_manager import SocketConnectionManager

class WebSocketHandler:
    '''
        Handles individual websockets
    '''

    def __init__(self):
        self.connection_manager = SocketConnectionManager()

    async def handle_connection(self, websocket: WebSocket):
        
        print(f"WebSocket type: {type(websocket)}")

        # Just for testing purposes, you can use a mock parameter check
        # without relying on query_params directly
        await self.connection_manager.connect(websocket)

        try:

            # Implement logic for chat between LLM's 
            while True:
                data = await websocket.receive_text()

                print(f"Received message from Client: {data}:")

                await websocket.send_text(f"Message from the server: received the following: {data}")

        except WebSocketDisconnect:
            self.connection_manager.disconnect(websocket)
            print("Client disconnected")

from fastapi import WebSocket, WebSocketDisconnect
from app.api.websocket.websocket_connection_manager import WebSocketConnectionManager
from app.core.session_manager import SessionManager

import aiofiles
import os
import bson

class WebSocketHandler:
    '''
        Handles individual websockets
    '''


    def __init__(self, session_manager: SessionManager):
        self.connection_manager = WebSocketConnectionManager()
        self.session_manager = session_manager
        self.pending_files = {}
        self.CONNECTED = True

    """

    The BSON message from front end requires

     - action : either being READY_FOR_FILE || TEXT_MESSAGE
            - This is to allow the backend to understand between the two types of data transfers
    """
    async def handle_connection(self, websocket: WebSocket):

        # without relying on query_params directly
        await websocket.accept()
        session_id = websocket.query_params.get("session_id")
        self.connection_manager.connect(websocket, session_id)

        try:
        
            # While connected to 
            while self.CONNECTED:

                session_id = websocket.query_params.get("session_id")
                self.check_session_id(websocket, session_id)

                data = await websocket.receive_bytes()
                message = bson.BSON(data).decode()

                if message.get("action") == "READY_FOR_FILE":

                    if session_id in self.pending_files:
                        await self.send_file(websocket, self.pending_files)
                        del self.pending_files
                    else:
                        await self.send_bson(websocket, {"type": "message", "content": "No file available yet."})
            
                elif message.get("action") == "TEXT_MESSAGE":
                    text_message = message.get("content", "")
                    await self.send_bson(websocket, {"type": "message", "content": f"Server received: {text_message}"})

        except WebSocketDisconnect:
            self.connection_manager.disconnect(websocket)
            print("Client disconnected")

    async def check_session_id(self, websocket: WebSocket, session_id: str) -> bool:
          
            if not session_id:
                self.connection_manager.disconnect(websocket)
                await websocket.close(code=4001, reason="Session ID is missing")
                return
            
            if not self.session_manager.validate_session(session_id):
                self.connection_manager.disconnect(websocket)
                await websocket.close(code=4002, reason="Invalid or expired session ID")
                return
            
    async def send_file(self, websocket: WebSocket, file_path: str):
        '''
            Sends a file via websocket
        '''

        if not os.path.exists(file_path):
            await self.send_bson(websocket, {"type": "errpr", "content": "File not found"})
            return
        
        try:
            filename = os.path.basename(file_path)
            await websocket.send_text(f"START_FILE_TRANSFER: {filename}")

            async with aiofiles.open(file_path, "rb") as file:
                file_data = await file.read

            bson_data = bson.BSON.encode({
                "type": "file",
                "filename": filename,
                "data": file_data
            })

            await websocket.send_bytes(bson_data)

        except Exception as e:
            await self.send_bson(websocket, {"type": "error", "content": str(e)})

    
    def notify_new_file(self, session_id: str, file_path: str):
        """
            Called by the LLM when new files of code snippets are available and ready
        """
        self.pending_files = file_path

    async def send_bson(self, websocket: WebSocket, message: dict):
        """
            Serializes and sends a BSON Message
        """
        bson_data = bson.BSON.encode(message)
        await websocket.send_bytes(bson_data)
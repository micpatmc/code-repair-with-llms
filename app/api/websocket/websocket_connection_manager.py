from fastapi import WebSocket, WebSocketDisconnect

class WebSocketConnectionManager:
    '''
        Manages websockets that are connected
        to the backend server
    '''

    def __init__(self):
        self.active_connections: Dict[str, Websocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        self.active_connections[session_id] = websocket
        print(f"Connection established for session: {session_id}")

    def disconnect(self, websocket: WebSocket):
        session_id = next((sid for sid, ws in self.active_connections.items() if ws == websocket), None)
        if session_id:
            del self.active_connections[session_id]
            print(f"Connection removed for session: {session_id}")


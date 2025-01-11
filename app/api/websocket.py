from fastapi import WebSocket, WebSocketDisconnect

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:

            data = await websocket.send_text("Connected to the backend server.")
            print(f"Connected to frontend: {data}")
            await websocket.send_text(f"Message received: {data}")
            
    except WebSocketDisconnect:
        print("Client Disconnected")

        
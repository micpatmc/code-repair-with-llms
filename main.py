from fastapi import FastAPI, WebSocket
from app.api.websocket_handler import WebSocketHandler
from app.api.rest.router import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Code Repair With LLM's",
    description="Backend server with LLM's"
)

# Allow all origins for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Manage websocket connections
websocket_manager = WebSocketHandler()

# Websocket for continued connection to backend
@app.websocket("/start-llm-session")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.handle_connection(websocket)

# For REST Api's 
app.include_router(api_router)


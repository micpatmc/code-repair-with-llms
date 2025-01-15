from fastapi import FastAPI
from app.api.websocket import websocket_endpoint
from app.api.router import api_router

app = FastAPI(
    title="Code Repair With LLM's",
    description="Backend server with LLM's"
)

# Websocket for continued connection to backend mostly used for chat
app.websocket("/start-llm-session")(websocket_endpoint)

# For REST Api's 
app.include_router(api_router)


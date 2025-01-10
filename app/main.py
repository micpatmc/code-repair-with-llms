from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(
    title="Code Repair With LLM's",
    description="Backend server for interaction of frontend with ARCC"
)

app.include_router(api_router)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import check_database

app = FastAPI(
    title="Drone Ecosystem API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Drone Ecosystem API is running"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/health/db")
async def database_health():
    if check_database():
        return {"database": "connected"}
    return {"database": "disconnected"}
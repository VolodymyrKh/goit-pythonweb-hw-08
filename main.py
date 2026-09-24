import uvicorn
from fastapi import FastAPI

from src.api import contacts, utils

app = FastAPI(
    title="Contacts API",
    description="REST API for storing and managing contacts",
    version="0.1.0",
)

app.include_router(utils.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

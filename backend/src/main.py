from fastapi import FastAPI
from backend.src.api import chatbot

app = FastAPI()

app.include_router(chatbot.router, prefix="/chat", tags=["Chatbot"])

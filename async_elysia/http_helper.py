import requests
import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()

BACKEND = "http://localhost:3001"
COMMAND_HISTORY_ADD = f"{BACKEND}/bots/command"
AUTH_KEY = os.getenv("AUTH_KEY")  # or hardcode if needed



async def get_self(auth_key):
    url = f"{BACKEND}/bots_auth/{auth_key}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            return None
        
def strip_mention(text: str) -> str:
    import re
    return re.sub(r'<@!?\d+>', '<USER>', text).strip()

async def send_command_log(payload: dict):
    print("Called Send")
    headers = {
        "Authorization": AUTH_KEY,
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(COMMAND_HISTORY_ADD, json=payload, headers=headers) as resp:
            try:
                return await resp.json()
            except:
                return await resp.text()
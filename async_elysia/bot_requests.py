import requests

def register(auth_key, discord_id, owner_id): 
    url = "http://localhost:3001/bots"

    payload = {
        "auth_key": auth_key,
        "bot_discord_id": discord_id,
        "owner_id": owner_id
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    print(response.json())

def get_self(auth_key):
    
    url = f"http://localhost:3001/bots_auth/{auth_key}"

    response = requests.get(url)

    print(response.json())
    return True if response.status_code == 200 else False
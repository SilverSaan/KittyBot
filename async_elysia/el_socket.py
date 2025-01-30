import asyncio
import websockets
import json
from discord.ext.commands import Bot


async def send_bot_status(bot_name, auth_token, bot, bot_status="online"):
    uri = "ws://localhost:3001/ws?auth_key=" + auth_token  # Send auth_key as a query param

    async with websockets.connect(uri) as websocket:
        async def send_status():
            """Send bot status updates every 5 seconds."""
            while True:
                status_data = {
                    "auth_key": auth_token,
                    "bot_status": bot_status,
                    "name": bot_name, 
                }
                await websocket.send(json.dumps(status_data))
                print(f"🔄 Sent status update: {status_data}")

                await asyncio.sleep(5)  # Wait for 5 seconds before sending the next update

        async def receive_messages():
            """Listen for messages from the server (e.g., shutdown command)."""
            async for response in websocket:
                print(f"📩 Server response: {response}")
                response_data = json.loads(response)

                if response_data.get("shutdown") == auth_token:
                    print("🛑 Shutdown signal received! Disconnecting...")

                    # Send offline status before shutting down
                    offline_status = {
                        "auth_key": auth_token,
                        "bot_status": "offline",
                        "name": bot_name, 
                    }
                    await websocket.send(json.dumps(offline_status))

                    await websocket.close()
                    await bot.close()
                    break  # Exit the receive loop

        # Run both tasks concurrently: send status updates & receive messages
        await asyncio.gather(send_status(), receive_messages())

async def run_task(bot_name, auth_token, bot: Bot): 
    asyncio.create_task(send_bot_status(bot_name, auth_token, bot))
    #asyncio.create_task(listen_for_shutdown(auth_token, bot))


def start_ws_run(bot_name, auth_token):
    asyncio.get_event_loop().run_until_complete(send_bot_status(bot_name, auth_token))


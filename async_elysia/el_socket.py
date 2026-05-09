import asyncio
import websockets
import json
from discord.ext.commands import Bot
from websockets.exceptions import ConnectionClosed


async def send_bot_status(bot_name, auth_token, bot, bot_status="online"):
    uri = f"ws://localhost:3001/ws?auth_key={auth_token}"
    
    while True:  # Outer loop for reconnection
        try:
            print(f"🔌 Attempting to connect to {uri}...")
            async with websockets.connect(uri) as websocket:
                print("✅ Connected to server.")

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
                        await asyncio.sleep(15)

                async def receive_messages():
                    """Listen for messages from the server."""
                    async for response in websocket:
                        print(f"📩 Server response: {response}")
                        response_data = json.loads(response)

                        if response_data.get("shutdown") == auth_token:
                            print("🛑 Shutdown signal received! Cleaning up...")
                            offline_status = {
                                "auth_key": auth_token,
                                "bot_status": "offline",
                                "name": bot_name, 
                            }
                            # Use a try/except here too in case the socket dies 
                            # exactly as we try to send the final "offline" msg
                            try:
                                await websocket.send(json.dumps(offline_status))
                                await websocket.close()
                            except:
                                pass
                            
                            await bot.close()
                            return "SHUTDOWN" # Signal to break the outer loop

                # gather(return_exceptions=False) means if one fails, gather raises it immediately
                # This is good because it triggers our outer 'except' block to reconnect
                done, pending = await asyncio.wait(
                    [asyncio.create_task(send_status()), 
                     asyncio.create_task(receive_messages())],
                    return_when=asyncio.FIRST_COMPLETED
                )

                # Clean up pending tasks
                for task in pending:
                    task.cancel()

                # Check if we exited because of a shutdown command
                for task in done:
                    if task.result() == "SHUTDOWN":
                        return 

        except (ConnectionClosed, OSError, ConnectionResetError) as e:
            print(f"⚠️ Connection lost ({e}). Retrying in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            await asyncio.sleep(5)

async def run_task(bot_name, auth_token, bot): 
    # Use create_task so it runs in the background of your main Discord bot
    asyncio.create_task(send_bot_status(bot_name, auth_token, bot))


def start_ws_run(bot_name, auth_token):
    asyncio.get_event_loop().run_until_complete(send_bot_status(bot_name, auth_token))


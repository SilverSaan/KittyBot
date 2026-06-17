import asyncio
import websockets
import json
from discord.ext.commands import Bot
from websockets.exceptions import ConnectionClosed


async def send_bot_status(bot_name, auth_token, bot: Bot, bot_status="online"):
    uri = f"ws://localhost:3001/ws?auth_key={auth_token}"
    
    guilds_data = [
        {"id": str(guild.id), "name": guild.name} 
        for guild in bot.guilds
    ]

    while True:
        try:
            print(f"🔌 Attempting to connect to {uri}...")
            async with websockets.connect(uri) as websocket:
                print("✅ Connected to server.")

                # Send identify once on connect
                await websocket.send(json.dumps({
                    "type": "identify",
                    "name": bot_name,
                    "discord_id": str(bot.user.id),
                    "guilds": guilds_data
                }))

                await setup_guild_events(bot, websocket, auth_token)

                async def send_ping():
                    """Send heartbeat ping every 20 seconds."""
                    while True:
                        await websocket.send(json.dumps({ "type": "ping" }))
                        print("🏓 Ping sent")
                        await asyncio.sleep(20)

                async def receive_messages():
                    """Listen for messages from the server."""
                    async for response in websocket:
                        print(f"📩 Server response: {response}")
                        response_data = json.loads(response)

                        if response_data.get("shutdown") == auth_token:
                            print("🛑 Shutdown signal received! Cleaning up...")
                            try:
                                await websocket.send(json.dumps({ "type": "offline" }))
                                await websocket.close()
                            except:
                                pass
                            
                            await bot.close()
                            return "SHUTDOWN"

                done, pending = await asyncio.wait(
                    [asyncio.create_task(send_ping()), 
                     asyncio.create_task(receive_messages())],
                    return_when=asyncio.FIRST_COMPLETED
                )

                for task in pending:
                    task.cancel()

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


async def setup_guild_events(bot, websocket, auth_token):
    
    @bot.event
    async def on_guild_join(guild):
        await websocket.send(json.dumps({
            "type": "guild_joined",
            "id": str(guild.id),
            "name": guild.name
        }))
        print(f"📥 Joined guild: {guild.name}")

    @bot.event
    async def on_guild_remove(guild):
        await websocket.send(json.dumps({
            "type": "guild_left",
            "id": str(guild.id),
        }))
        print(f"📤 Left guild: {guild.name}")
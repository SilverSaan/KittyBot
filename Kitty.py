import discord
import os
from discord.ext import commands
from discord import app_commands


import json


import traceback
import sys
import argparse

#Create token.json like {"discord_token": randToken, "owner_token": Owner Discord ID}
def get_tokens():
  with open('token.json') as f:
    return(json.load(f))
  
tokens = get_tokens()
DISCORD_TOKEN = tokens['discord_token']
AUTH_TOKEN = tokens['auth_key']
BOT_NAME = tokens['bot_name']

options = {
    "backend" : True, 
    "load_rolls": True,
    "load_book_table_generation": True,
    "verbose_debug": False
}

def get_data():
    role_skill = None
    role_stats = None
    skills = None
    current_dir = os.path.dirname(os.path.abspath(__file__))
    roles_path = os.path.join(current_dir, 'jsons', 'roles.json')
    stats_path = os.path.join(current_dir, 'jsons', 'statitics_role.json')
    skills_path = os.path.join(current_dir, 'jsons', 'skills.json')
    
    with open(roles_path) as f:
        role_skill = json.load(f)
    with open(stats_path) as f:
        role_stats = json.load(f)
    with open(skills_path) as f:
        skills = json.load(f)
    
    return role_skill, role_stats, skills

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=';', intents=intents)
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


async def load_cogs():
    # Imports
    from cogs.dice import DiceCommands
    from cogs.tablegen import TableGenerator
    from cogs.utilities import LunarUtils

    #Add Cogs
    await bot.add_cog(DiceCommands(bot))
    await bot.add_cog(LunarUtils(bot))

    await bot.add_cog(TableGenerator(bot, get_data))


@bot.hybrid_command()
async def hello(ctx):
  await ctx.send('Hello, my name is Kitty, Exotic from Biotechnica\'s Zoo and your resident Cyberpunk (Being cute doesn\'t pay rent) catgirl ≽^•⩊•^≼\n\n\
I can roll dice for you, and also generate some useful things (More to come btw), like Night Markets, NPC Ideas... aaaand that\'s it *ฅ^•ﻌ•^ฅ*\n\
If you want DnD utilities try to convince my creator @silversaan to develop my father (The Innkeeper / Tavern Bot)')

@bot.tree.command(name='sync', description='Owner only')
async def sync(interaction: discord.Interaction):
    if interaction.user.id == tokens['owner_token']:
        await bot.tree.sync(guild=None)
        await bot.tree.sync(guild=interaction.guild)
        await interaction.response.send_message('Command tree synced.')
        print('Command tree synced.')
    else:
        await interaction.response.send_message('You must be my owner to use this command!')

@bot.command()
async def sync(ctx):
    print("sync command")
    if ctx.author.id == tokens['owner_token']:
        await bot.tree.sync()
        await ctx.send('Command tree synced.')
    else:
        await ctx.send('You must be my owner to use this command!')

@bot.command()
async def shutdown(ctx):
    if ctx.author.id == tokens['owner_token']:
        await ctx.send('Shutting down... Bye bye!')
        await bot.close()
    else:
        await ctx.send('You must be my owner to use this command!')


@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        # User joined a voice channel
        print(f"{member.display_name} joined the voice channel {after.channel.name}")
    elif before.channel is not None and after.channel is None:
        # User left a voice channel
        print(f"{member.display_name} left the voice channel {before.channel.name}")
        
    
@bot.hybrid_command()
@commands.has_permissions(administrator=True)
async def notify_dm(ctx, role: discord.Role, message: str):
  members = role.members
  #print(members)
  for member in members:
    try:
      await member.send(message)
      await ctx.send(f"Message sent to {member.name}", ephemeral=True)
    except discord.Forbidden:
      await ctx.send(f"Failed to send message to {member.name}",ephemeral=True)


@notify_dm.error
async def notify_dm_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You must be an administrator to use this command.", ephemeral=True)

@bot.event
async def on_ready():
   print("Bot is ready and online")



@bot.event
async def on_command_error(ctx: commands.Context, error):
    error = getattr(error, 'original', error)
    
    # Ignore CommandNotFound errors (happens with slash commands or typos)
    if isinstance(error, commands.CommandNotFound):
        return
    
    # Handle your errors here
    if isinstance(error, commands.MemberNotFound):
        await ctx.send(f"I could not find member '{error.argument}'. Please try again")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"'{error.param.name}' is a required argument, choom.")
    
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command, choom.")
    
    else:
        # All unhandled errors will print their original traceback
        print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
        if options['verbose_debug']:
          traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


#GET SELF FROM BACKEND
async def connect_backend():
  print("Yo")
  import async_elysia.bot_requests as back_end
  from async_elysia.el_socket import send_bot_status, run_task
  bot_name = BOT_NAME
  auth_token = AUTH_TOKEN

  status = back_end.get_self(auth_token)  # True if registration successful, False otherwise

  if status:
      await run_task(bot_name, auth_token, bot) #Sends periodic status updates to the backend
      print("Bot registration successful. WebSocket connection established.")
  else:
      print("Bot registration failed. Running without backend access.")

@bot.event
async def on_ready():
    print("Bot is ready and online")
    await load_cogs()
     # Sync the command tree AFTER loading cogs
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

    if options['backend']:
      await connect_backend()


parser = argparse.ArgumentParser()
parser.add_argument("-nobe", "--no_backend", help="Ignores Connection to the Backend for telemetry and reduces noise on debug", action=argparse.BooleanOptionalAction)
parser.add_argument("-v", "--verbose", help="Debug will show every error, including ignored ones", action=argparse.BooleanOptionalAction)



if __name__ == "__main__":
  args = parser.parse_args()

  if args.no_backend: 
    options['backend'] = False
  if args.verbose: 
    options['verbose_debug'] = True

  bot.run(DISCORD_TOKEN)

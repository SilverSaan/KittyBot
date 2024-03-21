import discord
import os
from discord.ext import commands
from discord import app_commands
import night_market_generator as nmg

import Dice_Processing as die
import json
from red_die import red as red_roll
from streetrat_creator.streetrat import RoleSelectView

import traceback
import sys

#Create token.json like {"discord_token": randToken, "owner_token": Owner Discord ID}
def get_tokens():
  with open('token.json') as f:
    return(json.load(f))
  
tokens = get_tokens()
DISCORD_TOKEN = tokens['discord_token']



intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@bot.hybrid_command()
async def hello(ctx):
  await ctx.send('Hello, my name is Kitty, Exotic from Biotechnica\'s Zoo and your resident Cyberpunk (Being cute doesn\'t pay rent) catgirl ≽^•⩊•^≼\n\n\
I can roll dice for you, and also generate some useful things (More to come btw), like Night Markets, NPC Ideas... aaaand that\'s it \*ฅ^•ﻌ•^ฅ*\n\
If you want DnD utilities try to convince my creator @silversaan to develop my father (The Innkeeper / Tavern Bot)')

@bot.hybrid_command()
async def roll(ctx, *,message):
  
  try:
    message = message.replace(' ', '')
    _, response = die.format_roll(message)
    await ctx.send(f'**{ctx.author.mention} rolled: ' + response + '**')
  except Exception as e:
    await ctx.send(f"Error - {e}")

@bot.hybrid_command()
async def iscore(ctx):
  await ctx.send("I'm not supposed to be used for DnD but here's your Initial Scores for it choom. /ᐠ - ⩊ -マ Ⳋ\n" +
    die.initialScoreRoll())

@bot.tree.command(name='sync', description='Owner only')
async def sync(interaction: discord.Interaction):
    if interaction.user.id == tokens['owner_token']:
        await bot.tree.sync()
        await interaction.response.send_message('Command tree synced.')

        print('Command tree synced.')
    else:
        await interaction.response.send_message('You must be my owner to use this command!')

@bot.hybrid_command()
async def red(ctx, *, message):
  try:
    message = message.replace(' ', '')
    message_response, crit_message = red_roll(message)
    
    string_response = f'**{ctx.author.mention} rolled: ' + message_response + '**\n'
    if crit_message:
      string_response += crit_message
    await ctx.send(string_response)
  except Exception as e:
    await ctx.send(f"Error - {e}")

@bot.command()
async def sync(ctx):
    print("sync command")
    if ctx.author.id == tokens['owner_token']:
        await bot.tree.sync()
        await ctx.send('Command tree synced.')
    else:
        await ctx.send('You must be my owner to use this command!')

@bot.hybrid_command()
async def nightmarket(ctx):
  await ctx.send(f'**{ctx.author.mention}' + "Generating your Night Market, this will take only a sec ₍^ >ヮ<^₎ .ᐟ.ᐟ**")
  await ctx.send(nmg.main())
  
@bot.hybrid_command()
async def streetrat(ctx):
    roles = ["Solo", "Rockerboy", "Netrunner", "Tech", "Medtech", "Media", "Lawman", "Exec", "Fixer", "Nomad"]
    view = RoleSelectView()
    await ctx.send("Select a role:", view=view, ephemeral=True)
    
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        # User joined a voice channel
        print(f"{member.display_name} joined the voice channel {after.channel.name}")
    elif before.channel is not None and after.channel is None:
        # User left a voice channel
        print(f"{member.display_name} left the voice channel {before.channel.name}")
        
@bot.hybrid_command()
async def dchance(ctx,chance): 
  try:
    ch = None
    if(float(chance) < 1 and float(chance) > 0 ):
      ch = int(float(chance) * 100)
      await ctx.send(f"Assuming you meant {int(float(chance) * 10)}%")
    elif(int(chance) <= 100 and int(chance) >= 1):
      ch = int(float(chance))
    else:
      await ctx.send(f'{ctx.author.mention} please input a number between 1 and 100 choom')

    if(ch): 
      roll, value = die.roll_dice("1d100")
      if value <= ch: 
        await ctx.send(f'{ctx.author.mention} **Success!** Rolled a {value} on the chance of {ch}%! **You got it choom!**')
      if value > ch: 
        await ctx.send(f'{ctx.author.mention} **Failed!** Rolled a {value} on the chance of {ch}%! Did you forget your LUCK points?! ')
  except Exception as e:
    await ctx.send(f'{ctx.author.mention} please input a number between 1 and 100 choom')


@bot.event
async def on_ready():
   print("Bot is ready and online")

@bot.event
async def on_command_error(ctx: commands.Context, error):
  error = getattr(error, 'original', error)
  # Handle your errors here
  if isinstance(error, commands.MemberNotFound):
      await ctx.send("I could not find member '{error.argument}'. Please try again")

  elif isinstance(error, commands.MissingRequiredArgument):
      await ctx.send(f"'{error.param.name}' is a required argument, choom.")
  else:
      # All unhandled errors will print their original traceback
      print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
      traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


bot.run(DISCORD_TOKEN)
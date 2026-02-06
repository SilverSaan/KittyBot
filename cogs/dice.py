from discord.ext import commands
import Dice_Processing as die
from red_die import red as red_roll, get_head_injury, get_body_injury
import random

class DiceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command()
    async def roll(self, ctx, *, message):
        try:

            _, response = die.format_roll(message)
            await ctx.send(f'**{ctx.author.mention} rolled: \n' + response + '**')
        except Exception as e:
            await ctx.send(f"Error - {e}")
    
    @commands.hybrid_command()
    async def red(self, ctx, *, message):
        try:
            message = message.replace(' ', '')
            message_response, crit_message = red_roll(message)
            
            string_response = f'**{ctx.author.mention} rolled: ' + message_response + '**\n'
            if crit_message:
                string_response += crit_message
            await ctx.send(string_response)
        except Exception as e:
            await ctx.send("Invalid roll format.")
    
    @commands.hybrid_command()
    async def crithead(self, ctx):
        response = get_head_injury()
        await ctx.send(response)
    
    @commands.hybrid_command()
    async def critbody(self, ctx):
        response = get_body_injury()
        await ctx.send(response)

 
    @commands.hybrid_command()
    async def dchance(self, ctx, chance):
        try:
            f = float(chance)
            if 0 < f < 1:
                ch = int(f * 100)
                await ctx.send(f"Assuming you meant {ch}%")
            elif 1 <= f <= 100:
                ch = int(f)
            else:
                await ctx.send(f"{ctx.author.mention} please input a number between 1 and 100")
                return

            value = random.randint(1, 100)

            if value <= ch:
                await ctx.send(f"{ctx.author.mention} **Success!** Rolled {value} on the chance of {ch}%!")
            else:
                await ctx.send(f"{ctx.author.mention} **Failed!** Rolled {value} on the chance of {ch}%!")

        except ValueError:
            await ctx.send(f"{ctx.author.mention} please input a valid number")

    @commands.hybrid_command()
    async def iscore(self, ctx):
        """Generates Initial DND Scores"""
        await ctx.send("I'm not supposed to be used for DnD but here's your Initial Scores for it choom. /ᐠ - ⩊ -マ Ⳋ\n" +
            die.initialScoreRoll())  


async def setup(bot):
    await bot.add_cog(DiceCommands(bot))
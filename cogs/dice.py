from discord.ext import commands
import Dice_Processing as die
from red_die import red as red_roll, get_head_injury, get_body_injury

class DiceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command()
    async def roll(self, ctx, *, message):
        try:
            message = message.replace(' ', '')
            _, response = die.format_roll(message)
            await ctx.send(f'**{ctx.author.mention} rolled: ' + response + '**')
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
            await ctx.send(f"Error - {e}")
    
    @commands.hybrid_command()
    async def crithead(self, ctx):
        response = get_head_injury()
        await ctx.send(response)
    
    @commands.hybrid_command()
    async def critbody(self, ctx):
        response = get_body_injury()
        await ctx.send(response)

    @commands.hybrid_command()
    async def dchance(self,ctx,chance): 
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

    @commands.hybrid_command()
    async def iscore(self, ctx):
        """Generates Initial DND Scores"""
        await ctx.send("I'm not supposed to be used for DnD but here's your Initial Scores for it choom. /ᐠ - ⩊ -マ Ⳋ\n" +
            die.initialScoreRoll())  


async def setup(bot):
    await bot.add_cog(DiceCommands(bot))
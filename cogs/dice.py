import re
from discord.ext import commands
import Dice_Processing as die
from red_die import red as red_roll, get_head_injury, get_body_injury
import random
from async_elysia.http_helper import send_command_log

class DiceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log(self, ctx, command_name: str, response: str, request_message: str | None = None):
        try:
            await send_command_log({
                "command_name": command_name,
                "guild_discord_id": str(ctx.guild.id),
                "user_nickname": ctx.author.display_name,
                "request_message": request_message,
                "response": response,
            })
        except Exception:
            pass

    @commands.hybrid_command()
    async def roll(self, ctx, *, message):
        try:
            _, response = die.format_roll(message)
            out = f'**{ctx.author.mention} rolled: \n' + response + '**'
            await ctx.send(out)
            await self.log(ctx, "roll", out, message)
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
            await self.log(ctx, "red", string_response, message)
        except Exception as e:
            await ctx.send("Invalid roll format.")

    @commands.hybrid_command()
    async def crithead(self, ctx):
        response = get_head_injury()
        await ctx.send(response)
        await self.log(ctx, "crithead", response)

    @commands.hybrid_command()
    async def critbody(self, ctx):
        response = get_body_injury()
        await ctx.send(response)
        await self.log(ctx, "critbody", response)

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
                out = f"{ctx.author.mention} please input a number between 1 and 100"
                await ctx.send(out)
                return

            value = random.randint(1, 100)

            if value <= ch:
                out = f"{ctx.author.mention} **Success!** Rolled {value} on the chance of {ch}%!"
            else:
                out = f"{ctx.author.mention} **Failed!** Rolled {value} on the chance of {ch}%!"

            await ctx.send(out)
            await self.log(ctx, "dchance", out, chance)

        except ValueError:
            await ctx.send(f"{ctx.author.mention} please input a valid number")

    @commands.hybrid_command()
    async def iscore(self, ctx):
        """Generates Initial DND Scores"""
        response = die.initialScoreRoll()
        out = "I'm not supposed to be used for DnD but here's your Initial Scores for it choom. /ᐠ - ⩊ -マ Ⳋ\n" + response
        await ctx.send(out)
        await self.log(ctx, "iscore", out)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        expr = message.content.strip()

        if not die.DICE_EXPR_FULL.match(expr):
            return

        try:
            result, response = die.format_roll(expr)
            print(result)
            out = f"**{message.author.mention} rolled:**\n{response}"
            await message.channel.send(out)
            try:
                await send_command_log({
                    "command_name": "inline_roll",
                    "guild_discord_id": str(message.guild.id),
                    "user_nickname": message.author.display_name,
                    "request_message": expr,
                    "response": out,
                })
            except Exception:
                pass
        except Exception:
            return


async def setup(bot):
    await bot.add_cog(DiceCommands(bot))
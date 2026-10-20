import re
from discord.ext import commands
import Dice_Processing as die
from red_die import red as red_roll, skill_check as red_skill_check, get_head_injury, get_body_injury
import random
from async_elysia.http_helper import send_command_log, strip_mention

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
            await self.log(ctx, "roll", strip_mention(out), message)
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
            await self.log(ctx, "red", strip_mention(string_response), message)
        except Exception as e:
            await ctx.send("Invalid roll format.")

    @commands.hybrid_command()
    async def check(self, ctx, stat: int, skill: int, dv: int):
        """Roll a Cyberpunk RED skill check: STAT + Skill + 1d10 vs DV."""
        try:
            total, initial_roll, critical_roll, success = red_skill_check(stat, skill, dv)
            breakdown = f"1d10({initial_roll})"
            if critical_roll is not None:
                operator = "+" if initial_roll == 10 else "-"
                breakdown += f" {operator} 1d10({critical_roll})"
            breakdown += f" + STAT {stat} + Skill {skill} = {total} vs DV {dv}"
            outcome = "SUCCESS" if success else "FAILURE"
            if initial_roll == 10:
                outcome += " (Critical Success)"
            elif initial_roll == 1:
                outcome += " (Critical Failure)"
            out = f"**{ctx.author.mention} skill check:** {breakdown}\n**{outcome}**"
            await ctx.send(out)
            await self.log(ctx, "check", strip_mention(out), f"{stat} {skill} {dv}")
        except ValueError as e:
            await ctx.send(f"Invalid skill check: {e}")

    @commands.hybrid_command()
    async def crithead(self, ctx):
        response = get_head_injury()
        await ctx.send(response)
        await self.log(ctx, "crithead", strip_mention(response))

    @commands.hybrid_command()
    async def critbody(self, ctx):
        response = get_body_injury()
        await ctx.send(response)
        await self.log(ctx, "critbody", strip_mention(response))

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
            await self.log(ctx, "dchance", strip_mention(out), chance)

        except ValueError:
            await ctx.send(f"{ctx.author.mention} please input a valid number")

    @commands.hybrid_command()
    async def iscore(self, ctx):
        """Generates Initial DND Scores"""
        response = die.initialScoreRoll()
        out = "I'm not supposed to be used for DnD but here's your Initial Scores for it choom. /ᐠ - ⩊ -マ Ⳋ\n" + response
        await ctx.send(out)
        await self.log(ctx, "iscore", strip_mention(out))

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
                    "response": strip_mention(out),
                })
            except Exception:
                pass
        except Exception:
            return


async def setup(bot):
    await bot.add_cog(DiceCommands(bot))
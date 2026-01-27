from discord.ext import commands
import discord

import utils.streetslangdict as slang
from streetrat_creator.streetrat import RoleSelectView
from net_gen.netInterface import NetInterface
import night_market_generator as nmg


class TableGenerator(commands.Cog):
    def __init__(self, bot, get_data_fun):
        self.bot = bot
        self.get_data = get_data_fun
        self.skill_roles, self.stat_tables, self.skills = get_data_fun()
    
    @commands.hybrid_command()
    async def generate_name(self, ctx, type):
        import names # type: ignore
        if type.lower() == "fem": 
            await ctx.send(f"Generated Name: \'{names.get_full_name(gender='female')}\'")
        elif type.lower() == "male": 
            await ctx.send(f"Generated Name: \'{names.get_full_name(gender='male')}\' ")
        else:
            await ctx.send(f"Wrong Input Type should be 'fem' or 'male'")

    
    @commands.hybrid_command(name="streetslang", description="Look up Cyberpunk streetslang terms")
    async def streetslang(self, ctx, *, term: str = None):
        try:
            if term is None:
                # No argument, show help
                help_text = (
                    "**Streetslang Dictionary** ≽^•⩊•^≼\n\n"
                    "Usage:\n"
                    "`/streetslang [term]` - Look up a specific term\n"
                    "`/streetslang random` - Get a random term\n"
                    "`/streetslang search [query]` - Search for terms\n"
                    "`/streetslang list` - Show all terms (sent via DM)\n\n"
                    f"Total terms in dictionary: {slang.get_slang_count()}"
                )
                await ctx.send(help_text)
            
            elif term.lower() == "random":
                # Get random term
                result = slang.random_slang()
                await ctx.send(f"Random Streetslang:\n{result}")
            
            elif term.lower().startswith("search "):
            # Search for terms
                query = term[7:].strip()
                if not query:
                    await ctx.send("Please provide a search term. Usage: `/streetslang search [query]`")
                    return
                    
                matches = slang.search_slang(query)
                if matches:
                    # Limit to first 10 results to avoid spam
                    result_text = "\n".join(matches[:10])
                    if len(matches) > 10:
                        result_text += f"\n\n*...and {len(matches) - 10} more results. Try a more specific search.*"
                    await ctx.send(f"Search results for '{query}':\n{result_text}")
                else:
                    await ctx.send(f"No streetslang terms found matching '{query}', choom.")
                    
            elif term.lower() == "list":
                # Send full list via DM
                all_terms = slang.list_all_slang()
                
                # Split into chunks to avoid Discord's message length limit
                chunk_size = 20
                chunks = [all_terms[i:i + chunk_size] for i in range(0, len(all_terms), chunk_size)]
                
            try:
                await ctx.author.send("**Complete Streetslang Dictionary**\n\n")
                for i, chunk in enumerate(chunks):
                    message = "\n".join(chunk)
                    await ctx.author.send(message)
                    
                    await ctx.send(f"{ctx.author.mention} Check your DMs for the complete streetslang dictionary, choom! ≽^•⩊•^≼")
            except discord.Forbidden:
                await ctx.send("I couldn't DM you the list, choom. Make sure your DMs are open!")
                
            else:
                # Look up specific term
                result = slang.lookup_slang(term)
            if result:
                await ctx.send(result)
            else:
                await ctx.send(f"Sorry choom, '{term}' isn't in my streetslang dictionary. Try `/streetslang search {term}` to find similar terms.")
                
        except Exception as e:
            await ctx.send(f"Error processing streetslang command: {e}")

    @commands.hybrid_command()
    async def nightmarket(self, ctx):
        if ctx.interaction:
            await ctx.interaction.response.send_message(
                f'**{ctx.author.mention} Generating your Night Market, this will take only a sec ₍^ >ヮ<^₎ .ᐟ.ᐟ**'
            )
            await ctx.send(nmg.main())  # This becomes a followup automatically
        else:
            # Regular text command
            await ctx.send(f'**{ctx.author.mention} Generating your Night Market, this will take only a sec ₍^ >ヮ<^₎ .ᐟ.ᐟ**')
            await ctx.send(nmg.main())
            
    @commands.hybrid_command()
    async def streetrat(self,ctx):
        # roles = ["Solo", "Rockerboy", "Netrunner", "Tech", "Medtech", "Media", "Lawman", "Exec", "Fixer", "Nomad"]
        view = RoleSelectView(self.skill_roles, self.stat_tables, self.skills)
        await ctx.send("Select a role:", view=view, ephemeral=True)

    @commands.hybrid_command()
    async def netgen(self,ctx):
        view = NetInterface()
        await ctx.send("Select a Difficulty:", view=view, ephemeral=True)
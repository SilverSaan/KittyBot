import discord
from discord.ext import commands
from . import NetGenerator as netgen

class NetInterface(discord.ui.View): 
    
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self.difficulty = None
        self.floors = None
    
    async def generate_and_send(self, interaction, difficulty):
        try:
            self.difficulty = difficulty
            self.floors = netgen.getArchitecture()
            netgen.setIDs(self.floors)
            netgen.populateFloors(self.floors)
            
            arch = netgen.printArchitecture(self.floors)
            legend = netgen.printLegend(self.floors, self.difficulty)
            
            diff_info = netgen.DIFFICULTY_INFO[difficulty]
            output = f"**Network Architecture - {diff_info}**\n```\n{arch}```\n{legend}"
            
            await interaction.response.edit_message(content=output, view=None)
        except Exception as e:
            await interaction.response.edit_message(
                content=f"Error generating architecture: {e}\nTry again, choom!",
                view=None
            )
        
    @discord.ui.button(label='Basic', style=discord.ButtonStyle.blurple)
    async def chooseDifficultyBasic(self, interaction, button):
        await self.generate_and_send(interaction, 1)

    @discord.ui.button(label='Standard', style=discord.ButtonStyle.green)
    async def chooseDifficultyStandard(self, interaction, button):
        await self.generate_and_send(interaction, 2)
        
    @discord.ui.button(label='Uncommon', style=discord.ButtonStyle.secondary)
    async def chooseDifficultyUncommon(self, interaction, button):
        await self.generate_and_send(interaction, 3)
        
    @discord.ui.button(label='Advanced', style=discord.ButtonStyle.red)
    async def chooseDifficultyAdvanced(self, interaction, button):
        await self.generate_and_send(interaction, 4)
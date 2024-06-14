import discord
from discord.ext import commands

from . import NetGenerator as netgen

class NetInterface(discord.ui.View): 
    
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self.difficulty = None
        self.floors = None
        
    @discord.ui.button(label='Solo', style=discord.ButtonStyle.red)
    async def chooseDifficultyBasic(self, interaction, button):
        
        self.difficulty = 1
        self.floors = netgen.getArchitecture()
        netgen.setIDs(self.floors)
        netgen.populateFloors(self.floors)
        
        arch = netgen.printArchitecture(self.floors)
        legend = netgen.printLegend(self.floors, self.difficulty)
        
        print("DEBUG", arch)
        
        await interaction.response.edit_message(content=f"```{arch}``` \n\n {legend}", view=None)


    @discord.ui.button(label='Solo', style=discord.ButtonStyle.red)
    async def chooseDifficultyStandard(self, interaction, button):
        
        self.difficulty = 2
        
    @discord.ui.button(label='Solo', style=discord.ButtonStyle.red)
    async def chooseDifficultyUncommon(self, interaction, button):
        
        self.difficulty = 3
        
    @discord.ui.button(label='Solo', style=discord.ButtonStyle.red)
    async def chooseDifficultyAdvanced(self, interaction, button):
        
        self.difficulty = 4
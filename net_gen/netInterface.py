import discord
from discord.ext import commands
from . import NetGenerator as netgen
from . import net_visualizer_matplotlib as viz
import io

DIFFICULTY_INFO = {
    1: "Basic (DV6) | Normal interface level 2",
    2: "Standard (DV8) | Normal interface level 4 | Deadly: 2",
    3: "Uncommon (DV10) | Normal interface level 6 | Deadly: 4",
    4: "Advanced (DV12) | Normal interface level 8 | Deadly: 6"
}

class NetInterface(discord.ui.View): 
    
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self.difficulty = None
        self.floors = None
        self.show_visual = False  # Default to visual diagram
    
    async def generate_and_send(self, interaction, difficulty):
        """Common method to generate and send architecture"""
        try:
            # Defer the response immediately to prevent timeout
            await interaction.response.defer()
            
            self.difficulty = difficulty
            self.floors = netgen.getArchitecture()
            netgen.setIDs(self.floors)
            netgen.populateFloors(self.floors)
            
            diff_info = DIFFICULTY_INFO[difficulty]
            
            if self.show_visual:
                # Generate visual diagram
                img_bytes = viz.create_network_diagram_matplotlib(self.floors, self.difficulty)
                
                # Create Discord file
                file = discord.File(io.BytesIO(img_bytes), filename='netarch.png')
                
                # Get legend text
                legend = netgen.printLegend(self.floors, self.difficulty)
                
                # Create view with toggle button
                view = NetToggleView(self.floors, self.difficulty)
                
                await interaction.followup.edit_message(
                    message_id=interaction.message.id,
                    content=f"**Network Architecture - {diff_info}**\n\n{legend}",
                    attachments=[file],
                    view=view
                )
            else:
                # Generate ASCII diagram
                arch = netgen.printArchitecture(self.floors)
                legend = netgen.printLegend(self.floors, self.difficulty)
                
                output = f"**Network Architecture - {diff_info}**\n```\n{arch}```\n{legend}"
                
                # Create view with toggle button
                view = NetToggleView(self.floors, self.difficulty)
                
                await interaction.followup.edit_message(
                    message_id=interaction.message.id,
                    content=output,
                    view=view
                )
                
        except Exception as e:
            try:
                await interaction.followup.send(
                    content=f"Error generating architecture: {e}\nTry again, choom!",
                    ephemeral=True
                )
            except:
                # If followup also fails, try responding directly
                await interaction.response.send_message(
                    content=f"Error generating architecture: {e}\nTry again, choom!",
                    ephemeral=True
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


class NetToggleView(discord.ui.View):
    """View to toggle between visual and ASCII representation"""
    
    def __init__(self, floors, difficulty, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self.floors = floors
        self.difficulty = difficulty
        self.is_visual = True  # Currently showing visual
    
    @discord.ui.button(label='Show ASCII', style=discord.ButtonStyle.secondary, emoji='📝')
    async def toggle_ascii(self, interaction, button):
        """Toggle between ASCII and visual view"""
        try:
            await interaction.response.defer()
            
            diff_info = DIFFICULTY_INFO[self.difficulty]
            
            if self.is_visual:
                # Currently showing visual, switch to ASCII
                arch = netgen.printArchitecture(self.floors)
                legend = netgen.printLegend(self.floors, self.difficulty)
                
                output = f"**Network Architecture - {diff_info}**\n```\n{arch}```\n{legend}"
                
                # Update button to show visual option
                button.label = 'Show Visual'
                button.emoji = '🖼️'
                self.is_visual = False
                
                await interaction.followup.edit_message(
                    message_id=interaction.message.id,
                    content=output,
                    attachments=[],
                    view=self
                )
            else:
                # Currently showing ASCII, switch to visual
                img_bytes = viz.create_network_diagram_matplotlib(self.floors, self.difficulty)
                file = discord.File(io.BytesIO(img_bytes), filename='netarch.png')
                
                legend = netgen.printLegend(self.floors, self.difficulty)
                
                # Update button back to ASCII option
                button.label = 'Show ASCII'
                button.emoji = '📝'
                self.is_visual = True
                
                await interaction.followup.edit_message(
                    message_id=interaction.message.id,
                    content=f"**Network Architecture - {diff_info}**\n\n{legend}",
                    attachments=[file],
                    view=self
                )
        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)
    
    @discord.ui.button(label='Show Simple Map', style=discord.ButtonStyle.secondary, emoji='🗺️')
    async def toggle_simple(self, interaction, button):
        """Toggle to simple visual map"""
        try:
            await interaction.response.defer()
            
            img_bytes = viz.create_simple_network_diagram_matplotlib(self.floors, self.difficulty)
            file = discord.File(io.BytesIO(img_bytes), filename='netarch_simple.png')
            
            diff_info = DIFFICULTY_INFO[self.difficulty]
            legend = netgen.printLegend(self.floors, self.difficulty)
            
            await interaction.followup.edit_message(
                message_id=interaction.message.id,
                content=f"**Network Architecture Map - {diff_info}**\n\n{legend}",
                attachments=[file],
                view=self
            )
        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)
    
    @discord.ui.button(label='Regenerate', style=discord.ButtonStyle.green, emoji='🔄')
    async def regenerate(self, interaction, button):
        """Generate a new architecture with same difficulty"""
        try:
            await interaction.response.defer()
            
            self.floors = netgen.getArchitecture()
            netgen.setIDs(self.floors)
            netgen.populateFloors(self.floors)
            
            if self.is_visual:
                img_bytes = viz.create_network_diagram_matplotlib(self.floors, self.difficulty)
                file = discord.File(io.BytesIO(img_bytes), filename='netarch.png')
                
                diff_info = DIFFICULTY_INFO[self.difficulty]
                legend = netgen.printLegend(self.floors, self.difficulty)
                
                await interaction.followup.edit_message(
                    message_id=interaction.message.id,
                    content=f"**Network Architecture - {diff_info}**\n\n{legend}",
                    attachments=[file],
                    view=self
                )
            else:
                arch = netgen.printArchitecture(self.floors)
                legend = netgen.printLegend(self.floors, self.difficulty)
                
                diff_info = DIFFICULTY_INFO[self.difficulty]
                output = f"**Network Architecture - {diff_info}**\n```\n{arch}```\n{legend}"
                
                await interaction.followup.edit_message(
                    message_id=interaction.message.id,
                    content=output,
                    view=self
                )
        except Exception as e:
            await interaction.followup.send(f"Error regenerating: {e}", ephemeral=True)
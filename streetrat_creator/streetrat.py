import discord
from discord.ext import commands
import json
import os

from . import math_util as derived_stat 
import random

def get_data():
    role_skill = None
    role_stats = None
    current_dir = os.path.dirname(os.path.abspath(__file__))
    roles_path = os.path.join(current_dir, 'table', 'roles.json')
    stats_path = os.path.join(current_dir, 'table', 'statitics_role.json')
    
    with open(roles_path) as f:
        role_skill = json.load(f)
    with open(stats_path) as f:
        role_stats = json.load(f)
        
    return role_skill, role_stats

skills, stat_tables = get_data()

class RoleSelectView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.role = None
        self.stats = {"int": 6, "ref": 7, "dex": 7, "tech": 3, "cool": 8, "will": 6, "luck": 5, "move": 5, "body": 6, "emp": 5} #This is for example
        self.skill = None, 
        self.hp = None
        self.humanity = None
    
    
    def format_stats(self,stats): 
        stats_s = "\n"
        stats_s += f"INT: {stats['int']}\n"    
        stats_s += f"REF: {stats['ref']}\n"    
        stats_s += f"DEX: {stats['dex']}\n"    
        stats_s += f"TECH: {stats['tech']}\n"    
        stats_s += f"COOL: {stats['cool']}\n"    
        stats_s += f"WILL: {stats['will']}\n"    
        stats_s += f"LUCK: {stats['luck']}\n"    
        stats_s += f"MOVE: {stats['move']}\n"    
        stats_s += f"BODY: {stats['body']}\n"    
        stats_s += f"EMP: {stats['emp']}\n" 
        return stats_s   
    
    async def remove_view(self, interaction):
        await interaction.message.edit(view=None)

    #This probably has some better way to do it but Idk how and trying to initiate the buttons on a loop wasn't working
    @discord.ui.button(label='Solo', style=discord.ButtonStyle.primary)
    async def solo_button(self, interaction, button):
        self.role = "Solo"
        self.stats = random.choice(stat_tables["Solo"])
        self.skill = skills["Solo"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])
        await interaction.response.send_message(f"Selected role: Solo\nStats: {self.format_stats(self.stats)}\nSkill: {self.skill}\nHP: {self.hp}\nHumanity: {self.humanity}", ephemeral=True)
        self.clear_items()
        await self.remove_view(interaction)
        

    @discord.ui.button(label='Rockerboy', style=discord.ButtonStyle.primary)
    async def rockerboy_button(self, interaction, button):
        self.role = "Rockerboy"
        self.stats = random.choice(stat_tables["Rockerboy"])
        self.skill = skills["Rockerboy"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.send_message(f"Selected role: Rockerboy\nStats: {self.format_stats(self.stats)}\nSkill: {self.skill}\nHP: {self.hp}\nHumanity: {self.humanity}", ephemeral=True)
        self.clear_items()
        await self.remove_view(interaction)


    @discord.ui.button(label='Netrunner', style=discord.ButtonStyle.primary)
    async def netrunner_button(self, interaction, button):
        self.role = "Netrunner"
        self.stats = random.choice(stat_tables["Netrunner"])
        self.skill = skills["Netrunner"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.send_message(f"Selected role: Netrunner\nStats: {self.format_stats(self.stats)}\nSkill: {self.skill}\nHP: {self.hp}\nHumanity: {self.humanity}", ephemeral=True)
        self.clear_items()
        await self.remove_view(interaction)

    @discord.ui.button(label='Tech', style=discord.ButtonStyle.primary)
    async def tech_button(self, interaction, button):
        self.role = "Tech"
        self.stats = random.choice(stat_tables["Tech"])
        self.skill = skills["Tech"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.send_message(f"Selected role: Tech\nStats: {self.format_stats(self.stats)}\nSkill: {self.skill}\n\nHP: {self.hp}\nHumanity: {self.humanity}", ephemeral=True)
        self.clear_items()
        await self.remove_view(interaction)

    @discord.ui.button(label='Medtech', style=discord.ButtonStyle.primary)
    async def medtech_button(self, interaction, button):
        self.role = "Medtech"
        self.stats = random.choice(stat_tables["Medtech"])
        self.skill = skills["Medtech"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.send_message(f"Selected role: Medtech\nStats: {self.format_stats(self.stats)}\nSkill: {self.skill}\n\nHP: {self.hp}\nHumanity: {self.humanity}", ephemeral=True)
        self.clear_items()
        await self.remove_view(interaction)


    @discord.ui.button(label='Media', style=discord.ButtonStyle.primary)
    async def media_button(self, interaction, button):
        self.role = "Media"
        self.stats = random.choice(stat_tables["Media"])
        self.skill = skills["Media"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.send_message(f"Selected role: Media\nStats: {self.format_stats(self.stats)}\nSkill: {self.skill}\nHP: {self.hp}\nHumanity: {self.humanity}", ephemeral=True)
        self.clear_items()
        await self.remove_view(interaction)


    @discord.ui.button(label='Lawman', style=discord.ButtonStyle.primary)
    async def lawman_button(self, interaction, button):
        self.role = "Lawman"

        self.stats = random.choice(stat_tables["Lawman"])
        self.skill = skills["Lawman"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.send_message(f"Selected role: Lawman\nStats: {self.format_stats(self.stats)}\nSkill: {self.skill}\nHP: {self.hp}\nHumanity: {self.humanity}", ephemeral=True)
        self.clear_items()
        await self.remove_view(interaction)


    @discord.ui.button(label='Exec', style=discord.ButtonStyle.primary)
    async def exec_button(self, interaction, button):
        self.role = "Exec"
        self.stats = random.choice(stat_tables["Exec"])
        self.skill = skills["Exec"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.send_message(f"Selected role: Exec\nStats: {self.format_stats(self.stats)}\nSkill: {self.skill}\nHP: {self.hp}\nHumanity: {self.humanity}", ephemeral=True)
        self.clear_items()
        await self.remove_view(interaction)

    @discord.ui.button(label='Fixer', style=discord.ButtonStyle.primary)
    async def fixer_button(self, interaction, button):
        self.role = "Fixer"

        self.stats = random.choice(stat_tables["Fixer"])
        self.skill = skills["Fixer"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.send_message(f"Selected role: Fixer\nStats: {self.format_stats(self.stats)}\nSkill: {self.skill}\nHP: {self.hp}\nHumanity: {self.humanity}", ephemeral=True)
        self.clear_items()
        await self.remove_view(interaction)

    @discord.ui.button(label='Nomad', style=discord.ButtonStyle.primary)
    async def nomad_button(self, interaction, button):
        self.role = "Nomad"

        self.stats = random.choice(stat_tables["Nomad"])
        self.skill = skills["Nomad"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.send_message(f"Selected role: Nomad\nStats: {self.format_stats(self.stats)}\nSkill: {self.skill}\nHP: {self.hp}\nHumanity: {self.humanity}", ephemeral=True)
        self.clear_items()
        await self.remove_view(interaction)

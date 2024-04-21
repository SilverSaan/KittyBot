import discord
from discord.ext import commands
import json
import os

from . import math_util as derived_stat 
import random
from .string_formatter import format_stats, format_skills, string_result

def get_data():
    role_skill = None
    role_stats = None
    skills = None
    current_dir = os.path.dirname(os.path.abspath(__file__))
    roles_path = os.path.join(current_dir, 'table', 'roles.json')
    stats_path = os.path.join(current_dir, 'table', 'statitics_role.json')
    skills_path = os.path.join(current_dir, 'table', 'skills.json')
    
    with open(roles_path) as f:
        role_skill = json.load(f)
    with open(stats_path) as f:
        role_stats = json.load(f)
    with open(skills_path) as f:
        skills = json.load(f)
    
    return role_skill, role_stats, skills

skill_role, stat_tables, skills = get_data()

class RoleSelectView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.role = None
        self.stats = {"int": 6, "ref": 7, "dex": 7, "tech": 3, "cool": 8, "will": 6, "luck": 5, "move": 5, "body": 6, "emp": 5} #This is for example only
        self.skill = None, 
        self.hp = None
        self.humanity = None
        self.timeout = 30.0
    
    
    
    async def remove_view(self, interaction):
        await interaction.message.edit(view=None)

    #This probably has some better way to do it but Idk how and trying to initiate the buttons on a loop wasn't working
    @discord.ui.button(label='Solo', style=discord.ButtonStyle.red)
    async def solo_button(self, interaction, button):
        
        self.role = "Solo"
        self.stats = random.choice(stat_tables["Solo"])
        self.skill = skill_role["Solo"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])
        await interaction.response.edit_message(content=string_result(self.role, self.hp, self.humanity, self.skill, self.stats,skills), view=None)

    @discord.ui.button(label='Rockerboy', style=discord.ButtonStyle.red)
    async def rockerboy_button(self, interaction, button):
        self.role = "Rockerboy"
        self.stats = random.choice(stat_tables["Rockerboy"])
        self.skill = skill_role["Rockerboy"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.edit_message(content=string_result(self.role, self.hp, self.humanity, self.skill, self.stats,skills), view=None)


    @discord.ui.button(label='Netrunner', style=discord.ButtonStyle.red)
    async def netrunner_button(self, interaction, button):
        self.role = "Netrunner"
        self.stats = random.choice(stat_tables["Netrunner"])
        self.skill = skill_role["Netrunner"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.edit_message(content=string_result(self.role, self.hp, self.humanity, self.skill, self.stats,skills), view=None)

    @discord.ui.button(label='Tech', style=discord.ButtonStyle.red)
    async def tech_button(self, interaction, button):
        self.role = "Tech"
        self.stats = random.choice(stat_tables["Tech"])
        self.skill = skill_role["Tech"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.edit_message(content=string_result(self.role, self.hp, self.humanity, self.skill, self.stats,skills), view=None)
        

    @discord.ui.button(label='Medtech', style=discord.ButtonStyle.red)
    async def medtech_button(self, interaction, button):
        self.role = "Medtech"
        self.stats = random.choice(stat_tables["Medtech"])
        self.skill = skill_role["Medtech"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.edit_message(content=string_result(self.role, self.hp, self.humanity, self.skill, self.stats,skills), view=None)
        


    @discord.ui.button(label='Media', style=discord.ButtonStyle.red)
    async def media_button(self, interaction, button):
        self.role = "Media"
        self.stats = random.choice(stat_tables["Media"])
        self.skill = skill_role["Media"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.edit_message(content=string_result(self.role, self.hp, self.humanity, self.skill, self.stats,skills), view=None)
        


    @discord.ui.button(label='Lawman', style=discord.ButtonStyle.red)
    async def lawman_button(self, interaction, button):
        self.role = "Lawman"

        self.stats = random.choice(stat_tables["Lawman"])
        self.skill = skill_role["Lawman"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.edit_message(content=string_result(self.role, self.hp, self.humanity, self.skill, self.stats,skills), view=None)
        


    @discord.ui.button(label='Exec', style=discord.ButtonStyle.red)
    async def exec_button(self, interaction, button):
        self.role = "Exec"
        self.stats = random.choice(stat_tables["Exec"])
        self.skill = skill_role["Exec"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.edit_message(content=string_result(self.role, self.hp, self.humanity, self.skill, self.stats,skills), view=None)
        

    @discord.ui.button(label='Fixer', style=discord.ButtonStyle.red)
    async def fixer_button(self, interaction, button):
        self.role = "Fixer"

        self.stats = random.choice(stat_tables["Fixer"])
        self.skill = skill_role["Fixer"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.edit_message(content=string_result(self.role, self.hp, self.humanity, self.skill, self.stats,skills), view=None)
        

    @discord.ui.button(label='Nomad', style=discord.ButtonStyle.red)
    async def nomad_button(self, interaction, button):
        self.role = "Nomad"

        self.stats = random.choice(stat_tables["Nomad"])
        self.skill = skill_role["Nomad"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.edit_message(content=string_result(self.role, self.hp, self.humanity, self.skill, self.stats,skills), view=None)
        self.stop()

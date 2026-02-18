import discord
from discord.ext import commands
import json
import os

from . import math_util as derived_stat 
import random
from .string_formatter import format_stats, format_skills, string_result


class RoleSelectView(discord.ui.View):
    def __init__(self, skill_role, stat_tables, skills):
        super().__init__()
        self.role = None
        self.stats = {"int": 6, "ref": 7, "dex": 7, "tech": 3, "cool": 8, "will": 6, "luck": 5, "move": 5, "body": 6, "emp": 5} #This is for example only
        self.skill = None, 
        self.hp = None
        self.humanity = None
        self.timeout = 30.0
        self.skill_role = skill_role
        self.stat_tables = stat_tables
        self.skills = skills

    async def remove_view(self, interaction):
        await interaction.message.edit(view=None)

    #This probably has some better way to do it but Idk how and trying to initiate the buttons on a loop wasn't working
    @discord.ui.button(label='Solo', style=discord.ButtonStyle.red)
    async def solo_button(self, interaction, button):
        
        self.role = "Solo"
        self.stats = random.choice(self.stat_tables["Solo"])
        self.skill = self.skill_role["Solo"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])
        await interaction.response.edit_message(content=string_result(self.role, self.hp, self.humanity, self.skill, self.stats,self.skills), view=None)

    @discord.ui.button(label='Rockerboy', style=discord.ButtonStyle.red)
    async def rockerboy_button(self, interaction, button):
        self.role = "Rockerboy"
        self.stats = random.choice(self.stat_tables["Rockerboy"])
        self.skill = self.skill_role["Rockerboy"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.edit_message(content=string_result(self.role, self.hp, self.humanity, self.skill, self.stats,self.skills), view=None)


    @discord.ui.button(label='Netrunner', style=discord.ButtonStyle.red)
    async def netrunner_button(self, interaction, button):
        self.role = "Netrunner"
        self.stats = random.choice(self.stat_tables["Netrunner"])
        self.skill = self.skill_role["Netrunner"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.edit_message(content=string_result(self.role, self.hp, self.humanity, self.skill, self.stats,self.skills), view=None)

    @discord.ui.button(label='Tech', style=discord.ButtonStyle.red)
    async def tech_button(self, interaction, button):
        self.role = "Tech"
        self.stats = random.choice(self.stat_tables["Tech"])
        self.skill = self.skill_role["Tech"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.edit_message(content=string_result(self.role, self.hp, self.humanity, self.skill, self.stats,self.skills), view=None)
        

    @discord.ui.button(label='Medtech', style=discord.ButtonStyle.red)
    async def medtech_button(self, interaction, button):
        self.role = "Medtech"
        self.stats = random.choice(self.stat_tables["Medtech"])
        self.skill = self.skill_role["Medtech"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.edit_message(content=string_result(self.role, self.hp, self.humanity, self.skill, self.stats,self.skills), view=None)
        


    @discord.ui.button(label='Media', style=discord.ButtonStyle.red)
    async def media_button(self, interaction, button):
        self.role = "Media"
        self.stats = random.choice(self.stat_tables["Media"])
        self.skill = self.skill_role["Media"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.edit_message(content=string_result(self.role, self.hp, self.humanity, self.skill, self.stats,self.skills), view=None)
        


    @discord.ui.button(label='Lawman', style=discord.ButtonStyle.red)
    async def lawman_button(self, interaction, button):
        self.role = "Lawman"

        self.stats = random.choice(self.stat_tables["Lawman"])
        self.skill = self.skill_role["Lawman"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.edit_message(content=string_result(self.role, self.hp, self.humanity, self.skill, self.stats,self.skills), view=None)
        


    @discord.ui.button(label='Exec', style=discord.ButtonStyle.red)
    async def exec_button(self, interaction, button):
        self.role = "Exec"
        self.stats = random.choice(self.stat_tables["Exec"])
        self.skill = self.skill_role["Exec"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.edit_message(content=string_result(self.role, self.hp, self.humanity, self.skill, self.stats,self.skills), view=None)
        

    @discord.ui.button(label='Fixer', style=discord.ButtonStyle.red)
    async def fixer_button(self, interaction, button):
        self.role = "Fixer"

        self.stats = random.choice(self.stat_tables["Fixer"])
        self.skill = self.skill_role["Fixer"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.edit_message(content=string_result(self.role, self.hp, self.humanity, self.skill, self.stats,self.skills), view=None)
        

    @discord.ui.button(label='Nomad', style=discord.ButtonStyle.red)
    async def nomad_button(self, interaction, button):
        self.role = "Nomad"

        self.stats = random.choice(self.stat_tables["Nomad"])
        self.skill = self.skill_role["Nomad"]
        self.hp = derived_stat.calculate_hp(self.stats["body"], self.stats["will"])
        self.humanity = derived_stat.calculate_humanity(self.stats["emp"])

        await interaction.response.edit_message(content=string_result(self.role, self.hp, self.humanity, self.skill, self.stats,self.skills), view=None)
        self.stop()

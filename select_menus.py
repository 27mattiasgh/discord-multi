import time
import random
import discord
from datetime import datetime
from discord import app_commands
from discord.ext import commands

from discord import ui
from discord.ui import ChannelSelect




class TestSelection(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=45)

    @ui.select(cls=ChannelSelect, placeholder="Select a Channel", channel_types=[discord.ChannelType.text])
    async def select_callback(self, interaction:discord.Interaction, select):
        channel = discord.utils.get(interaction.guild.channels, name=str(select.values[0]))

        return await interaction.response.send_message(f"Verify Channel Set: <#{channel.id}>")




class Wager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="testing", description="testing")
    async def testing(self, interaction: discord.Interaction):


        return await interaction.response.send_message("Testing", view=TestSelection(), ephemeral=True)






from discord import ui

class Questionnaire(ui.Modal, title='Questionnaire Response'):
    name = ui.TextInput(label='Name')
    answer = ui.TextInput(label='Answer', style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)



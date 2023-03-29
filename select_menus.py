import time
import random
import discord
from datetime import datetime
from discord import app_commands
from discord.ext import commands





class TestSelection(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=45)

    options_list = ["Option 1", "Option 2", "Option 3"]

    @discord.ui.select(placeholder = "Select a Move", min_values = 1, max_values = 1, 
                       
                       options = [discord.SelectOption(label=str(option), description=f"Move {option}") for option in options_list]

                       )
    
    async def select_callback(self, interaction:discord.Interaction, select):
        return await interaction.response.send_message(f"{select.values[0]}")






class Wager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="testing", description="testing")
    async def testing(self, interaction: discord.Interaction):
        return await interaction.response.send_message("Testing", view=TestSelection(), ephemeral=True)






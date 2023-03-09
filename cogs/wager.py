import random
import discord
from discord import app_commands
from discord.ext import commands





class TestSelection(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=45)

    options_list = []

    @discord.ui.select(placeholder = "Select a Move", min_values = 1, max_values = 1, 
                       
                       options = [discord.SelectOption(label=str(option), description=f"Move {option}") for option in options_list]

                       )
    


    async def select_callback(self, interaction:discord.Interaction, select):
        self.options_list.append(4)
        return await interaction.response.send_message(f"{select.values[0]}, list: ")






class Wager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @app_commands.command(name="test", description="testing")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message('Hi!', view=TestSelection())

#build chess board using ascii

#check for win using engine.py
       


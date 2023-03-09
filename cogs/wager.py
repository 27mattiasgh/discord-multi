import random
import discord
from discord import app_commands
from discord.ext import commands





class TestSelection(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=45)
        self.options_list = [1, 2, 3]

    @discord.ui.select(placeholder="Choose a Flavor!", min_values=1, max_values=1)
    async def select_callback(self, select: discord.ui.Select):
        # Generate the options list dynamically
        options = [discord.SelectOption(label=str(option), description=f"Option {option}") for option in self.options_list]

        # Set the options for the select menu
        select.options = options

        # Wait for the user to make a selection
        await select.prompt.send()

        # Send a message with the selected value
        await select.response.send_message(f"You selected {select.values[0]}")







class Wager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @app_commands.command(name="test", description="testing")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message('Hi!', view=TestSelection)

    
       


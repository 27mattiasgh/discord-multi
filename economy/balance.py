import json
import discord
from discord import app_commands
from discord.ext import commands


class Balance(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot



    @app_commands.command(name="balance", description="view your balance")
    async def balance(self, interaction: discord.Interaction, user:discord.User=None):

        if user is None:
            user = interaction.user
            
        with open('resources\economy.json', 'r') as f:
            data = json.load(f)

        await interaction.response.send_message(content=data['users'][str(user.id)]['balance'], ephemeral=True)




    @app_commands.command(name="add_balance", description="add to your balance")
    async def add_balance(self, interaction: discord.Interaction, amount:int, user:discord.User=None):

        if user is None:
            user = interaction.user
            
        with open('resources\economy.json', 'r') as f:
            data = json.load(f)

        

        data['users'][str(user.id)]['balance'] += amount

        new_balance = data['users'][str(user.id)]['balance']

        with open('resources\economy.json', 'w') as f:
            json.dump(data, f)


        await interaction.response.send_message(f'Current balance: {new_balance}', ephemeral=True)
        
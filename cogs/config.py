import json
import discord
from discord import app_commands
from discord.ext import commands



class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)


    @discord.ui.button(label="Reset Infractions",style=discord.ButtonStyle.red)
    async def reset_infractions(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild = interaction.guild
        infraction_counts = {}
        for member in guild.members:
            infraction_counts[member.id] = 0
        with open('infractions.json', 'w') as f:
            json.dump(infraction_counts, f)
            
        await interaction.response.edit_message(content='`infractions.json reset`')



class Config(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.command(name="config", description="administator permissions required")
    async def config(self, interaction: discord.Interaction):
        embedVar = discord.Embed(color=0x009a00)
        await interaction.response.send_message('`press buttons below to edit config files`', view=Buttons(), ephemeral=True)


    

    
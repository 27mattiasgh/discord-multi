import time
import random
import discord
from datetime import datetime
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

        emoji = [":gem:", ":first_place:", ":100:", ":dollar:", ":moneybag:", ":bell:"]
        one, two, three = random.choice(emoji), random.choice(emoji), random.choice(emoji)

        embedVar = discord.Embed(color=0x009a00)
        embedVar.add_field(name="Slot Machine!", value=f"<a:slot:1084337026586914857>|<a:slot:1084337026586914857>|<a:slot:1084337026586914857>")
        await interaction.response.send_message(embed=embedVar)
        time.sleep(1.5)

        embedVar = discord.Embed(color=0x009a00)
        embedVar.add_field(name="Slot Machine!", value=f"{one}|<a:slot:1084337026586914857>|<a:slot:1084337026586914857>")
        await interaction.edit_original_response(embed=embedVar)
        time.sleep(1.5)

        embedVar = discord.Embed(color=0x009a00)
        embedVar.add_field(name="Slot Machine!", value=f"{one}|{two}|<a:slot:1084337026586914857>")
        await interaction.edit_original_response(embed=embedVar)
        time.sleep(1.5)


        embedVar = discord.Embed(color=0x009a00)
        if one == two == three:
            embedVar.add_field(name="Jackpot!", value=f"{one}|{two}|{three}")
            return await interaction.edit_original_response(embed=embedVar)

        if one == two or one == three or two == three:
            embedVar.add_field(name="Close!", value=f"{one}|{two}|{three}")
            return await interaction.edit_original_response(embed=embedVar)

        else:
            embedVar = discord.Embed(color=0x009a00)
            embedVar.set_thumbnail(url='https://cdn.discordapp.com/attachments/1081307005018439821/1084349448882245712/slot-machine-emoji-clipart-md.png')
            embedVar.add_field(name="Slot Machine", value=f"""**
            ---------
            {one}|{two}|{three}
            ---------**""")
            return await interaction.edit_original_response(embed=embedVar)



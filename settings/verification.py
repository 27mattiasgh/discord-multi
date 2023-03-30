import io
import json
import discord
import random
import string
from PIL import Image, ImageDraw, ImageFont

from discord import app_commands
from discord.utils import get
from discord.ext import commands
from discord import ui
from discord.ui import RoleSelect


class SetupButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)

    @discord.ui.button(label="Set Role", custom_id='change_role', style=discord.ButtonStyle.grey)
    async def change_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        embedVar = discord.Embed(color=0x89CFF0, description="Select the verification role using the drop-down below:")
        await interaction.response.edit_message(embed=embedVar, view=RoleSelection())

    @discord.ui.button(label="Create Role", custom_id='create_role', style=discord.ButtonStyle.grey)
    async def create_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = await interaction.guild.create_role(name="Not Verified", color=0x89CFF0)
        for chan in interaction.guild.channels:
            await chan.set_permissions(role, read_messages=False)

        with open(r'settings\verification.json', 'r') as f:
            data = json.load(f)
        data[str(interaction.guild.id)]['settings']['role'] = str(role.id)

        with open(r'settings\verification.json', 'w') as f:
            json.dump(data, f)

        self.create_role.disabled = True
        self.change_role.disabled = True    
        embedVar = discord.Embed(color=0x89CFF0, description=f"<@&{role.id}> Created\n\nIf you want to customize the name and color of the role in the server settings, you can do so according to your preference. Please note that the bot requires the role ID, which means that you can restore the role quickly by running the same command in case of accidental deletion. ")
        await interaction.response.edit_message(embed=embedVar, view=self)
        
    @discord.ui.button(label="Update", custom_id='done', style=discord.ButtonStyle.green)
    async def done(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open(r'settings\verification.json', 'r') as f:
            data = json.load(f)   

        embedVar = discord.Embed(color=0x89CFF0, description=f'''Verification Changes Saved\n\n**Verification Role:** <@&{int(data[str(interaction.guild.id)]['settings']['role'])}>''')
        return await interaction.response.edit_message(embed=embedVar, view=self, delete_after=10) 

class RoleSelection(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=45)

    @ui.select(cls=RoleSelect, placeholder="Select a Role", min_values=1, max_values=1)
    async def select_callback(self, interaction:discord.Interaction, select):
        
        with open(r'settings\verification.json', 'r') as f:
            data = json.load(f)

        role = discord.utils.get(interaction.guild.roles, name=str(select.values[0]))
        data[str(interaction.guild.id)]["settings"]['role'] = str(role.id)

        with open(r'settings\verification.json', 'w') as f:
            json.dump(data, f)

        channel = f"""<#{data[str(interaction.guild.id)]["settings"]['channel']}>""" if data[str(interaction.guild.id)]["settings"]['channel'] else 'None'
        role = f"""<@&{data[str(interaction.guild.id)]['settings']['role']}>""" if data[str(interaction.guild.id)]['settings']['role'] else 'None'
        embedVar = discord.Embed(color=0x89CFF0, title="Verification Setup", description=f"""Press the buttons to edit the respective verification values.\n**Verification Channel:** None -> {channel}\n**Verification Role:** None -> {role}""")
        return await interaction.response.edit_message(embed=embedVar, view=SetupButtons())

class Verification(commands.GroupCog, group_name='verification'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open(r'settings\verification.json', 'r') as f:
            data = json.load(f)
        data[str(guild.id)] = {"settings": {"channel": None, "role": None}, "keys": {}}
        with open(r'settings\verification.json', 'w') as f:
            json.dump(data, f)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        with open(r'settings\verification.json', 'r') as f:
            data = json.load(f)

        user_id = str(member.id)
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        data[str(member.guild.id)]['keys'][user_id] = password
        verify_channel_id = data[str(member.guild.id)]['settings']['channel']

        with open(r'settings\verification.json', 'w') as f:
            json.dump(data, f)

        image = Image.new('RGB', (400, 200), color=(43, 45, 49))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", size=38)
        position = (120, 75)
        color = (255, 255, 255)
        draw.text(position, password, fill=color, font=font)

        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        img_buffer.seek(0)

        guild = self.bot.get_guild(int(member.guild.id))
        role = get(guild.roles, id=int(data[str(guild.id)]['settings']['role']))
        await member.add_roles(role, reason='Verification')

        dm = await member.create_dm()
        embedVar = discord.Embed(color=0x89CFF0, title="Verification", description=f"Welcome to **{member.guild}**! To verify, refer to the image below and enter the code into this DM channel using `/verify`. If you aren't able to gain access, please refer to the information located in the verification channel.")
        embedVar.set_image(url="attachment://password.png")
        return await dm.send(file=discord.File(img_buffer, "password.png"), embed=embedVar)

    @app_commands.command(name="verify", description="Verify process for new users. The phrase parameter is the code you received from the bot.")
    async def verify(self, interaction: discord.Interaction, phrase:str):
        with open(r'settings\verification.json', 'r') as f:
            data = json.load(f)

        valid = False
        if interaction.channel.type ==  discord.ChannelType.private:
            for guild_id, guild_data in data.items():
                if str(interaction.user.id) in guild_data["keys"]:
                    phrase_found = guild_data["keys"][str(interaction.user.id)]
                    if phrase == phrase_found:
                        phrase = phrase_found
                        guild_id = int(guild_id)
                        valid = True

        if not valid:
            embedVar = discord.Embed(color=0xFFC0CB, description=f"Verification was not successful. Try again or contact the administrator.\n\nYou entered: **{phrase}**")
            return await interaction.response.send_message(embed=embedVar, delete_after=5)
        
        guild = self.bot.get_guild(int(guild_id))
        member = guild.get_member(interaction.user.id)
        role = get(guild.roles, id=int(data[str(guild_id)]['settings']['role']))
        await member.remove_roles(role, reason='Verification')

        data[str(guild.id)]['keys'].pop(str(member.id), None)
        with open(r'settings\verification.json', 'w') as f:
            json.dump(data, f)

        embedVar = discord.Embed(color=0x89CFF0, description=f"Verification Confirmed. Welcome to **{guild}**!")
        await interaction.response.send_message(embed=embedVar)

    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.command(name="settings", description="Configure verification settings. Requires kick permissions.")
    async def settings(self, interaction: discord.Interaction):
            embedVar = discord.Embed(color=0x89CFF0, title="Verification Settings", description="Press the buttons to edit the respective verification values.")
            return await interaction.response.send_message(embed=embedVar, view=SetupButtons(), ephemeral=True)       
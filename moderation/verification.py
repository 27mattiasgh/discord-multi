import io
import json
import sys
import discord
import random
import string
from PIL import Image, ImageDraw, ImageFont

from discord import app_commands
from discord.utils import get
from discord.ext import commands


class Verification(commands.GroupCog, group_name='verification'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        with open(r'C:\Users\Mati\OneDrive\Desktop\Discord Slash Commands\moderation\verification.json', 'r') as f:
            data = json.load(f)

        user_id = str(member.id)
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        data['user_keys'][user_id] = password
        verify_channel_id = data['server_settings']['channel']
        with open(r'C:\Users\Mati\OneDrive\Desktop\Discord Slash Commands\moderation\verification.json', 'w') as f:
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

        dm = await member.create_dm()
        embedVar = discord.Embed(color=0x89CFF0, title="Verification", description=f"Welcome to **{member.guild}**! To verify, refer to the image below and enter the code into <#{verify_channel_id}>. If you aren't able to gain access, please refer to the information located in the verification channel.")
        embedVar.set_image(url="attachment://password.png")


        return await dm.send(file=discord.File(img_buffer, "password.png"), embed=embedVar)

    @commands.Cog.listener()
    async def on_message(self, message):
        with open(r'C:\Users\Mati\OneDrive\Desktop\Discord Slash Commands\moderation\verification.json', 'r') as f:
            data = json.load(f)
        if message.channel.id == data["server_settings"].get('channel'):

            user_id = str(message.author.id)
            password = data["user_keys"].get(user_id)

            if password is not None and message.content == password:
                #adds role
                role = get(message.author.guild.roles, id=data["server_settings"]['role'])
                await message.author.add_roles(role)

                #resets json
                data['user_keys'].pop(str(message.author.id), None)
                with open(r'C:\Users\Mati\OneDrive\Desktop\Discord Slash Commands\moderation\verification.json', 'w') as f:
                    json.dump(data, f)

                embedVar = discord.Embed(color=0x89CFF0, description=f"Verification Confirmed. Welcome to **{message.guild}**!")

            else:
                embedVar = discord.Embed(color=0xFFC0CB, description=f"Verification was not successful. Try again or contact the administrator.")

            dm = await message.author.create_dm()
            await dm.send(embed=embedVar)
            await message.delete()
            
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.command(name="set_channel", description="Sets the verification channel. Requires kick permissions.")
    async def set_verification_channel(self, interaction: discord.Interaction, channel:discord.TextChannel):

        with open(r'C:\Users\Mati\OneDrive\Desktop\Discord Slash Commands\moderation\verification.json', 'r') as f:
            data = json.load(f)
        data["server_settings"]['channel'] = channel.id

        with open(r'C:\Users\Mati\OneDrive\Desktop\Discord Slash Commands\moderation\verification.json', 'w') as f:
            json.dump(data, f)

        embedVar = discord.Embed(color=0x89CFF0, title=f"Verification Channel Set!",description=f"Verification channel set to <#{channel.id}>.")
        embedVar.set_footer(text=f'{interaction.user.display_name}#{interaction.user.discriminator}')

        return await interaction.response.send_message(embed=embedVar, ephemeral=True)



        with open(r'C:\Users\Mati\OneDrive\Desktop\Discord Slash Commands\moderation\verification.json', 'r') as f:
            data = json.load(f)
        data["server_settings"]['log_channel'] = channel.id

        with open(r'C:\Users\Mati\OneDrive\Desktop\Discord Slash Commands\moderation\verification.json', 'w') as f:
            json.dump(data, f)

        embedVar = discord.Embed(color=0x89CFF0, title=f"Verification Channel Set!",description=f"Verification log channel set to <#{channel.id}>.")
        embedVar.set_footer(text=f'{interaction.user.display_name}#{interaction.user.discriminator}')

        return await interaction.response.send_message(embed=embedVar, ephemeral=True)
    
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.command(name="set_role", description="Sets the verification role. Requires kick permissions.")
    async def set_verification_role(self, interaction: discord.Interaction, role:discord.Role):

        with open(r'C:\Users\Mati\OneDrive\Desktop\Discord Slash Commands\moderation\verification.json', 'r') as f:
            data = json.load(f)
        data["server_settings"]['role'] = role.id

        with open(r'C:\Users\Mati\OneDrive\Desktop\Discord Slash Commands\moderation\verification.json', 'w') as f:
            json.dump(data, f)

        embedVar = discord.Embed(color=0x89CFF0, title=f"Verification Role Set!",description=f"Verification role set to <@&{role.id}>.")
        embedVar.set_footer(text=f'{interaction.user.display_name}#{interaction.user.discriminator}')

        return await interaction.response.send_message(embed=embedVar, ephemeral=True)
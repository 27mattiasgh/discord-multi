import io, os
import json
import discord
import random
import string
import pymongo
from pymongo import MongoClient
from PIL import Image, ImageDraw, ImageFont

from discord import app_commands
from discord.utils import get
from discord.ext import commands

uri = "mongodb+srv://Mati:55Ls4ey2W2YTPMQd@cluster0.xrwgmqb.mongodb.net/Data?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.Data


guild_collection = db.verification


def add_guild(server_id, role_id):
    guild_collection.insert_one({'_id': server_id, 'role': role_id})

def find_guild(user_id):
    users = guild_collection.find({'_id': {'$regex': f'.*_{user_id}_verification'}})
    guilds = {user['_id'].split('_')[0] for user in users}
    guild_id = int(list(guilds)[0])
    return guild_id


def add_user(server_id, user_id, phrase=None):
    user = guild_collection.find_one({'_id': f"{server_id}_{user_id}_verification"})
    if user:
        guild_collection.delete_one({'_id': f"{server_id}_{user_id}_verification"})
        return
    guild_collection.insert_one({'_id': f"{server_id}_{user_id}_verification", 'phrase': phrase})


def check_phrase(server_id, user_id, phrase):
    user = guild_collection.find_one({'_id': f"{server_id}_{user_id}_verification"})
    return True if user['phrase'] == phrase else False


def update_role(server_id, new_role_id):
    print(new_role_id, 'attemping to update role')


    if guild_collection.find_one({'_id': server_id}): 

        print(new_role_id, 'update role func')


        guild_collection.update_one({'_id': server_id}, {'$set': {'role': new_role_id}})
        
    else: 
        print('trying...')
        add_guild(server_id, new_role_id)
        print('guild not present in database, added guild!')

def get_role(server_id):
    guild = guild_collection.find_one({'_id': server_id})
    return guild['role'] if guild else None



class SetupButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)

    @discord.ui.button(label='Create Role', custom_id='create_role', style=discord.ButtonStyle.grey)
    async def create_role(self, interaction: discord.Interaction, button: discord.ui.Button):

        role = await interaction.guild.create_role(name='Verified', color=0x89CFF0)

        for chan in interaction.guild.channels:

            if chan.permissions_for(interaction.guild.default_role).read_messages and chan.permissions_for(role).read_messages:
                await chan.set_permissions(interaction.guild.default_role, read_messages=False)
                await chan.set_permissions(role, read_messages=True)

        update_role(interaction.guild.id, role.id)

        embed = discord.Embed(color=0x89CFF0, description=f'<@&{role.id}> Created\n\nIf you want to customize the name and color of the role in the server settings, you can do so according to your preference. Please note that the bot requires the role ID, which means that you can restore the role quickly by running the same command in case of accidental deletion. ')
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Update', custom_id='done', style=discord.ButtonStyle.green)
    async def done(self, interaction: discord.Interaction, button: discord.ui.Button):


        embed = discord.Embed(color=0x89CFF0, description=f"""Verification Changes Saved!""")
        return await interaction.response.edit_message(embed=embed, view=self, delete_after=10) 

class Verification(commands.GroupCog, group_name='verification'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print(f'Class {self.__class__.__name__} loaded.')


    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        guild = self.bot.get_guild(member.guild.id)
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        add_user(guild.id, member.id, password)

        image = Image.new('RGB', (400, 200), color=(43, 45, 49))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('arial.ttf', size=38)
        position = (120, 75)
        color = (255, 255, 255)
        draw.text(position, password, fill=color, font=font)

        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        img_buffer.seek(0)

        dm = await member.create_dm()
        embed = discord.Embed(color=0x89CFF0, title='Verification', description=f"Welcome to **{member.guild}**! To verify, refer to the image below and enter the code into this DM channel using `/verify`. If you aren't able to gain access, please refer to the information located in the verification channel.")
        embed.set_image(url='attachment://password.png')
        return await dm.send(file=discord.File(img_buffer, 'password.png'), embed=embed)





    @app_commands.command(name='verify', description='Verify process for new users. The phrase parameter is the code you received from the bot.')
    async def verify(self, interaction: discord.Interaction, phrase:str):
        guild = self.bot.get_guild(find_guild(interaction.user.id))


        if not check_phrase(guild.id, interaction.user.id, phrase):
            embed = discord.Embed(color=0xFFC0CB, description=f'Verification was not successful. Try again or contact the administrator.\n\nYou entered: **{phrase}**')
            return await interaction.response.send_message(embed=embed, delete_after=5, ephemeral=True)
        


        role = get(guild.roles, id=get_role(guild.id))


        if role is None:
            role = await guild.create_role(name='Verified', color=0x89CFF0)
            print(role.id)

            for chan in guild.channels:
                if chan.permissions_for(interaction.guild.default_role).read_messages and chan.permissions_for(role).read_messages:
                    await chan.set_permissions(interaction.guild.default_role, read_messages=False)
                    await chan.set_permissions(role, read_messages=True)


            print('updating role still in main')
            update_role(guild.id, role.id)


        member = guild.get_member(interaction.user.id)
        print(member.name, 'member name')

        await member.add_roles(role)
        print('added role to member')

        add_user(guild.id, interaction.user.id)

        embed = discord.Embed(color=0x89CFF0, description=f'Verification Confirmed. Welcome to **{guild}**!')

        await member.send(embed=embed)





    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.command(name='settings', description='Configure verification settings. Requires kick permissions.')
    async def settings(self, interaction: discord.Interaction):
            embed = discord.Embed(color=0x89CFF0, title='Verification Settings', description='Press the buttons to edit the respective verification values.')
            return await interaction.response.send_message(embed=embed, view=SetupButtons(), ephemeral=True)    
import io
import os
import random
import time
import requests
import discord
from discord import app_commands
from discord.ext import commands

import pymongo
from pymongo import MongoClient
from PIL import Image, ImageDraw, ImageFont

uri = "mongodb+srv://Mati:55Ls4ey2W2YTPMQd@cluster0.xrwgmqb.mongodb.net/Data?retryWrites=true&w=majority"
client = MongoClient(uri)

db = client.Data
collection = db.users

script_dir = os.path.dirname(os.path.abspath(__file__))
rank_image_path = os.path.join(script_dir, "rank.png")
rank_image = Image.open(rank_image_path)

font_path = os.path.join(script_dir, "font.ttf")

#DATABASE CONFIGURATION
def add_user(server_id, user_id):
    collection.insert_one({'_id': user_id, 'guild': server_id, 'score': 0, 'balance': 0,'primary': (255, 255, 255), 'secondary': (0, 0, 0)})


def get_user_rank_position(user_id, guild_id):
    scores = list(collection.find().sort('score', -1))
    user_score = next((s for s in scores if s['_id'] == user_id and s['guild'] == guild_id), None)

    if user_score: user_position = scores.index(user_score) + 1
    return user_position

def add_rank_score(server_id, user_id):
    collection.update_one({'_id': user_id, 'guild': server_id}, {'$inc': {'score': 1}})

def get_rank_score(server_id, user_id):
    user = collection.find_one({'_id': user_id, 'guild': server_id})
    if user: return user['score']
    else: return None

def get_profile_colors(server_id, user_id):
    query = {"guild": server_id, "_id": user_id}
    docs = collection.find(query)

    for doc in docs:
        primary = doc["primary"]
        secondary = doc["secondary"]
        return tuple(primary), tuple(secondary)

def update_profile_colors(server_id, user_id, primary, secondary):
    query = {'guild': server_id, '_id': user_id}
    update = {'$set': {'primary': primary, 'secondary': secondary}}
    collection.update_one(query, update)




def get_economy_balance(server_id, user_id):
    user = collection.find_one({'_id': user_id, 'guild': server_id})
    if user: return user['balance']
    else: return None

def configure_economy_balance(server_id, user_id, amount: int):
    amount = 0 if get_economy_balance(server_id, user_id) + amount < 0 and amount < 0 else amount
    collection.update_one({'_id': user_id, 'guild': server_id}, {'$inc': {'balance': amount}}) 



def get_economy_inventory(server_id, user_id):
    user = collection.find_one({'_id': user_id, 'guild': server_id})
    if user: return user['inventory']
    else: return None  

def check_economy_inventory(server_id, user_id, item):
    user = collection.find_one({'_id': user_id, 'guild': server_id})
    return True if item in user['inventory'] else False

def configure_economy_inventory(server_id, user_id, item, action):
    new = get_economy_inventory(server_id, user_id).append(item) if action == 'add' else get_economy_inventory(server_id, user_id).remove(item)
    collection.update_one({'_id': user_id, 'guild': server_id}, {'$inc': {'inventory': new}}) 





#OTHER FUNCTIONS
def create_rank_image(level, username, user_id, server_id, progress, primary_color, secondary_color, pfp_path):
    background_color = (primary_color)
    image_size = (600, 120)
    image = Image.new("RGB", image_size, background_color)

    draw = ImageDraw.Draw(image)


    pfp = Image.open(pfp_path).convert("RGBA")
    pfp_size = (80, 80)
    pfp = pfp.resize(pfp_size, Image.ANTIALIAS)

    mask = Image.new("L", pfp.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, pfp.size[0], pfp.size[1]), fill=255)
    pfp.putalpha(mask)

    border_size = 6
    bordered_pfp_size = (pfp_size[0] + border_size * 2, pfp_size[1] + border_size * 2)
    bordered_pfp = Image.new("RGBA", bordered_pfp_size, (137, 207, 240, 0))

    bordered_pfp.paste(pfp, (border_size, border_size), pfp)
    image.paste(bordered_pfp, (20, (image_size[1] - bordered_pfp_size[1]) // 2), bordered_pfp)
    

    font = ImageFont.truetype(font_path, size=20)
    draw.text((130, 25), username, font=font, fill=(255, 255, 255))

    draw.text((400, 25), f"Rank #{get_user_rank_position(user_id, server_id)}", font=font, fill=secondary_color)
    draw.text((500, 25), f"Level {level}", font=font, fill=secondary_color)

    bar_width = 450
    bar_height = 30

    bar_x = 130

    bar_y = ((image.height - bar_height) // 2) + 20

    bar_radius = bar_height // 2
    bar_end = bar_x + bar_width  
    bar_progress_end = bar_x + int(bar_width * progress)  # Right end of the progress
    draw.rounded_rectangle((bar_x, bar_y, bar_end, bar_y + bar_height), radius=bar_radius, outline=(255, 255, 255))
    draw.rounded_rectangle((bar_x, bar_y, bar_progress_end, bar_y + bar_height), radius=bar_radius, fill=secondary_color)

    return image

class ColorButtons(discord.ui.View):
    def __init__(self, mode, primary, secondary):

        super().__init__(timeout=None)
        self.mode = mode
        self.primary = primary
        self.secondary = secondary

        self.red_middle.label = self.primary[0] if self.mode == 'primary' else self.secondary[0]
        self.green_middle.label = self.primary[1] if self.mode == 'primary' else self.secondary[1]
        self.blue_middle.label = self.primary[2] if self.mode == 'primary' else self.secondary[2]

        self.red_minus_10.disabled = False
        self.red_minus_1.disabled = False
        self.red_plus_1.disabled = False
        self.red_plus_10.disabled = False

        self.green_minus_10.disabled = False
        self.green_minus_1.disabled = False
        self.green_plus_1.disabled = False
        self.green_plus_10.disabled = False

        self.blue_minus_10.disabled = False
        self.blue_minus_1.disabled = False
        self.blue_plus_1.disabled = False
        self.blue_plus_10.disabled = False

    #SELECTION MENUS
        if self.mode == 'primary':
            self.primary_selection.value = discord.ButtonStyle.green
            self.secondary_selection.value = discord.ButtonStyle.gray

        if self.mode == 'secondary':
            self.primary_selection.value = discord.ButtonStyle.gray
            self.secondary_selection.value = discord.ButtonStyle.green

        

    #PLUS 1
        if self.primary[0] + 1 > 255 and self.mode == 'primary':
            self.red_plus_1.disabled = True

        if self.primary[1] + 1 > 255 and self.mode == 'primary':
            self.green_plus_1.disabled = True
                    
        if self.primary[2] + 1 > 255 and self.mode == 'primary':
            self.blue_plus_1.disabled = True

        if self.secondary[0] + 1 > 255 and self.mode == 'secondary':
            self.red_plus_1.disabled = True

        if self.secondary[1] + 1 > 255 and self.mode == 'secondary':
            self.green_plus_1.disabled = True
                    
        if self.secondary[2] + 1 > 255 and self.mode == 'secondary':
            self.blue_plus_1.disabled = True

    #PLUS 10    
        if self.primary[0] + 10 > 255 and self.mode == 'primary':
            self.red_plus_10.disabled = True

        if self.primary[1] + 10 > 255 and self.mode == 'primary':
            self.green_plus_10.disabled = True
                    
        if self.primary[2] + 10 > 255 and self.mode == 'primary':
            self.blue_plus_10.disabled = True

        if self.secondary[0] + 10 > 255 and self.mode == 'secondary':
            self.red_plus_10.disabled = True

        if self.secondary[1] + 10 > 255 and self.mode == 'secondary':
            self.green_plus_10.disabled = True
                    
        if self.secondary[2] + 10 > 255 and self.mode == 'secondary':
            self.blue_plus_10.disabled = True

    #MINUS 1
        if self.primary[0] - 1 < 0 and self.mode == 'primary':
            self.red_minus_1.disabled = True

        if self.primary[1] - 1 < 0 and self.mode == 'primary':
            self.green_minus_1.disabled = True
                    
        if self.primary[2] - 1 < 0 and self.mode == 'primary':
            self.blue_minus_1.disabled = True

        if self.secondary[0] - 1 < 0 and self.mode == 'secondary':
            self.red_minus_1.disabled = True

        if self.secondary[1] - 1 < 0 and self.mode == 'secondary':
            self.green_minus_1.disabled = True
                    
        if self.secondary[2] - 1 < 0 and self.mode == 'secondary':
            self.blue_minus_1.disabled = True

    #MINUS 10    
        if self.primary[0] - 10 < 0 and self.mode == 'primary':
            self.red_minus_10.disabled = True

        if self.primary[1] - 10 < 0 and self.mode == 'primary':
            self.green_minus_10.disabled = True
                    
        if self.primary[2] - 10 < 0 and self.mode == 'primary':
            self.blue_minus_10.disabled = True

        if self.secondary[0] - 10 < 0 and self.mode == 'secondary':
            self.red_minus_10.disabled = True

        if self.secondary[1] - 10 < 0 and self.mode == 'secondary':
            self.green_minus_10.disabled = True
                    
        if self.secondary[2] - 10 < 0 and self.mode == 'secondary':
            self.blue_minus_10.disabled = True

    #ABOVE SELECTOR
    @discord.ui.button(label='Primary Color', style=discord.ButtonStyle.grey, custom_id='primary_selection', row=0)
    async def primary_selection(self, interaction: discord.Interaction, button: discord.ui.Button):
        pfp_response = requests.get(interaction.user.avatar.url)
        pfp_path = "pfp.png"
        with open(pfp_path, "wb") as f: f.write(pfp_response.content)
        primary, secondary = tuple(self.primary), tuple(self.secondary)
        image = create_rank_image(99, str(interaction.user.name)+'#'+str(interaction.user.discriminator), interaction.user.id, interaction.guild.id, 0.5, primary, secondary, pfp_path)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(buffer, filename="rank.png")
        embed = discord.Embed(color=0x89CFF0, description="Use the buttons below to edit the respective color values. Keep in mind the rank bar below is only an example; you must click `save` to save the colors to your profile.")
        embed.set_image(url="attachment://rank.png")
        await interaction.response.edit_message(embed=embed, attachments=[file], view=ColorButtons('primary', self.primary, self.secondary))

    @discord.ui.button(label='Secondary Color', style=discord.ButtonStyle.grey, custom_id='secondary_selection', row=0)
    async def secondary_selection(self, interaction: discord.Interaction, button: discord.ui.Button):
        pfp_response = requests.get(interaction.user.avatar.url)
        pfp_path = "pfp.png"
        with open(pfp_path, "wb") as f: f.write(pfp_response.content)
        primary, secondary = tuple(self.primary), tuple(self.secondary)
        image = create_rank_image(99, str(interaction.user.name)+'#'+str(interaction.user.discriminator), interaction.user.id, interaction.guild.id, 0.5, primary, secondary, pfp_path)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(buffer, filename="rank.png")
        embed = discord.Embed(color=0x89CFF0, description="Use the buttons below to edit the respective color values. Keep in mind the rank bar below is only an example; you must click `save` to save the colors to your profile.")
        embed.set_image(url="attachment://rank.png")
        await interaction.response.edit_message(embed=embed, attachments=[file], view=ColorButtons('secondary', self.primary, self.secondary))

    @discord.ui.button(label='Reset', style=discord.ButtonStyle.grey, custom_id='reset', row=0)
    async def reset(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.primary = [100, 100, 100]
        self.secondary = [200, 100, 100]
        
        pfp_response = requests.get(interaction.user.avatar.url)
        pfp_path = "pfp.png"
        with open(pfp_path, "wb") as f: f.write(pfp_response.content)
        primary, secondary = tuple(self.primary), tuple(self.secondary)
        image = create_rank_image(99, str(interaction.user.name)+'#'+str(interaction.user.discriminator), interaction.user.id, interaction.guild.id, 0.5, primary, secondary, pfp_path)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(buffer, filename="rank.png")
        embed = discord.Embed(color=0x89CFF0, description="Use the buttons below to edit the respective color values. Keep in mind the rank bar below is only an example; you must click `save` to save the colors to your profile.")
        embed.set_image(url="attachment://rank.png")
        await interaction.response.edit_message(embed=embed, attachments=[file], view=ColorButtons(self.mode, self.primary, self.secondary))
    
    @discord.ui.button(label='Save', style=discord.ButtonStyle.grey, custom_id='save', row=0)
    async def save(self, interaction: discord.Interaction, button: discord.ui.Button):
        primary = tuple(self.primary)
        secondary = tuple(self.secondary)
        update_profile_colors(interaction.guild.id, interaction.user.id, primary, secondary)

        embed = discord.Embed(color=0x89CFF0, description="Profile color values updated!")
        return await interaction.response.edit_message(embed=embed)

    #RED UI
    @discord.ui.button(label='-10', style=discord.ButtonStyle.red, custom_id='red_minus_10', row=1)
    async def red_minus_10(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.mode == 'primary':
            self.primary[0] -= 10

        if self.mode == 'secondary':
            self.secondary[0] -= 10

        pfp_response = requests.get(interaction.user.avatar.url)
        pfp_path = "pfp.png"
        with open(pfp_path, "wb") as f: f.write(pfp_response.content)
        primary, secondary = tuple(self.primary), tuple(self.secondary)
        image = create_rank_image(99, str(interaction.user.name)+'#'+str(interaction.user.discriminator), interaction.user.id, interaction.guild.id, 0.5, primary, secondary, pfp_path)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(buffer, filename="rank.png")
        embed = discord.Embed(color=0x89CFF0, description="Use the buttons below to edit the respective color values. Keep in mind the rank bar below is only an example; you must click `save` to save the colors to your profile.")
        embed.set_image(url="attachment://rank.png")
        await interaction.response.edit_message(embed=embed, attachments=[file], view=ColorButtons(self.mode, self.primary, self.secondary))

    @discord.ui.button(label='-1', style=discord.ButtonStyle.red, custom_id='red_minus_1', row=1)
    async def red_minus_1(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.mode == 'primary':
            self.primary[0] -= 1

        if self.mode == 'secondary':
            self.secondary[0] -= 1

        pfp_response = requests.get(interaction.user.avatar.url)
        pfp_path = "pfp.png"
        with open(pfp_path, "wb") as f: f.write(pfp_response.content)
        primary, secondary = tuple(self.primary), tuple(self.secondary)
        image = create_rank_image(99, str(interaction.user.name)+'#'+str(interaction.user.discriminator), interaction.user.id, interaction.guild.id, 0.5, primary, secondary, pfp_path)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(buffer, filename="rank.png")
        embed = discord.Embed(color=0x89CFF0, description="Use the buttons below to edit the respective color values. Keep in mind the rank bar below is only an example; you must click `save` to save the colors to your profile.")
        embed.set_image(url="attachment://rank.png")
        await interaction.response.edit_message(embed=embed, attachments=[file], view=ColorButtons(self.mode, self.primary, self.secondary))


    @discord.ui.button(label='ㅤ', style=discord.ButtonStyle.red, custom_id='red_middle', disabled=True, row=1)
    async def red_middle(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label='+1', style=discord.ButtonStyle.red, custom_id='red_plus_1', row=1)
    async def red_plus_1(self, interaction: discord.Interaction, button: discord.ui.Button):


        if self.mode == 'primary':
            self.primary[0] += 1

        if self.mode == 'secondary':
            self.secondary[0] += 1

        pfp_response = requests.get(interaction.user.avatar.url)
        pfp_path = "pfp.png"
        with open(pfp_path, "wb") as f: f.write(pfp_response.content)
        primary, secondary = tuple(self.primary), tuple(self.secondary)
        image = create_rank_image(99, str(interaction.user.name)+'#'+str(interaction.user.discriminator), interaction.user.id, interaction.guild.id, 0.5, primary, secondary, pfp_path)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(buffer, filename="rank.png")
        embed = discord.Embed(color=0x89CFF0, description="Use the buttons below to edit the respective color values. Keep in mind the rank bar below is only an example; you must click `save` to save the colors to your profile.")
        embed.set_image(url="attachment://rank.png")
        await interaction.response.edit_message(embed=embed, attachments=[file], view=ColorButtons(self.mode, self.primary, self.secondary))

    @discord.ui.button(label='+10', style=discord.ButtonStyle.red, custom_id='red_plus_10', row=1)
    async def red_plus_10(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.mode == 'primary':
            self.primary[0] += 10

        if self.mode == 'secondary':
            self.secondary[0] += 10

        pfp_response = requests.get(interaction.user.avatar.url)
        pfp_path = "pfp.png"
        with open(pfp_path, "wb") as f: f.write(pfp_response.content)
        primary, secondary = tuple(self.primary), tuple(self.secondary)
        image = create_rank_image(99, str(interaction.user.name)+'#'+str(interaction.user.discriminator), interaction.user.id, interaction.guild.id, 0.5, primary, secondary, pfp_path)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(buffer, filename="rank.png")
        embed = discord.Embed(color=0x89CFF0, description="Use the buttons below to edit the respective color values. Keep in mind the rank bar below is only an example; you must click `save` to save the colors to your profile.")
        embed.set_image(url="attachment://rank.png")
        await interaction.response.edit_message(embed=embed, attachments=[file], view=ColorButtons(self.mode, self.primary, self.secondary))

    #GREEN UI
    @discord.ui.button(label='-10', style=discord.ButtonStyle.green, custom_id='green_minus_10', row=2)
    async def green_minus_10(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.mode == 'primary':
            self.primary[1] -= 10

        if self.mode == 'secondary':
            self.secondary[1] -= 10

        pfp_response = requests.get(interaction.user.avatar.url)
        pfp_path = "pfp.png"
        with open(pfp_path, "wb") as f: f.write(pfp_response.content)
        primary, secondary = tuple(self.primary), tuple(self.secondary)
        image = create_rank_image(99, str(interaction.user.name)+'#'+str(interaction.user.discriminator), interaction.user.id, interaction.guild.id, 0.5, primary, secondary, pfp_path)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(buffer, filename="rank.png")
        embed = discord.Embed(color=0x89CFF0, description="Use the buttons below to edit the respective color values. Keep in mind the rank bar below is only an example; you must click `save` to save the colors to your profile.")
        embed.set_image(url="attachment://rank.png")
        await interaction.response.edit_message(embed=embed, attachments=[file], view=ColorButtons(self.mode, self.primary, self.secondary))

    @discord.ui.button(label='-1', style=discord.ButtonStyle.green, custom_id='green_minus_1', row=2)
    async def green_minus_1(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.mode == 'primary':
            self.primary[1] -= 1

        if self.mode == 'secondary':
            self.secondary[1] -= 1

        pfp_response = requests.get(interaction.user.avatar.url)
        pfp_path = "pfp.png"
        with open(pfp_path, "wb") as f: f.write(pfp_response.content)
        primary, secondary = tuple(self.primary), tuple(self.secondary)
        image = create_rank_image(99, str(interaction.user.name)+'#'+str(interaction.user.discriminator), interaction.user.id, interaction.guild.id, 0.5, primary, secondary, pfp_path)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(buffer, filename="rank.png")
        embed = discord.Embed(color=0x89CFF0, description="Use the buttons below to edit the respective color values. Keep in mind the rank bar below is only an example; you must click `save` to save the colors to your profile.")
        embed.set_image(url="attachment://rank.png")
        await interaction.response.edit_message(embed=embed, attachments=[file], view=ColorButtons(self.mode, self.primary, self.secondary))
   
    @discord.ui.button(label='ㅤ', style=discord.ButtonStyle.green, custom_id='green_middle', disabled=True, row=2)
    async def green_middle(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label='+1', style=discord.ButtonStyle.green, custom_id='green_plus_1', row=2)
    async def green_plus_1(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.mode == 'primary':
            self.primary[1] += 1

        if self.mode == 'secondary':
            self.secondary[1] += 1

        pfp_response = requests.get(interaction.user.avatar.url)
        pfp_path = "pfp.png"
        with open(pfp_path, "wb") as f: f.write(pfp_response.content)
        primary, secondary = tuple(self.primary), tuple(self.secondary)
        image = create_rank_image(99, str(interaction.user.name)+'#'+str(interaction.user.discriminator), interaction.user.id, interaction.guild.id, 0.5, primary, secondary, pfp_path)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(buffer, filename="rank.png")
        embed = discord.Embed(color=0x89CFF0, description="Use the buttons below to edit the respective color values. Keep in mind the rank bar below is only an example; you must click `save` to save the colors to your profile.")
        embed.set_image(url="attachment://rank.png")
        await interaction.response.edit_message(embed=embed, attachments=[file], view=ColorButtons(self.mode, self.primary, self.secondary))

    @discord.ui.button(label='+10', style=discord.ButtonStyle.green, custom_id='green_plus_10', row=2)
    async def green_plus_10(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.mode == 'primary':
            self.primary[1] += 10

        if self.mode == 'secondary':
            self.secondary[1] += 10

        pfp_response = requests.get(interaction.user.avatar.url)
        pfp_path = "pfp.png"
        with open(pfp_path, "wb") as f: f.write(pfp_response.content)
        primary, secondary = tuple(self.primary), tuple(self.secondary)
        image = create_rank_image(99, str(interaction.user.name)+'#'+str(interaction.user.discriminator), interaction.user.id, interaction.guild.id, 0.5, primary, secondary, pfp_path)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(buffer, filename="rank.png")
        embed = discord.Embed(color=0x89CFF0, description="Use the buttons below to edit the respective color values. Keep in mind the rank bar below is only an example; you must click `save` to save the colors to your profile.")
        embed.set_image(url="attachment://rank.png")
        await interaction.response.edit_message(embed=embed, attachments=[file], view=ColorButtons(self.mode, self.primary, self.secondary))

    #BLUE UI
    @discord.ui.button(label='-10', style=discord.ButtonStyle.blurple, custom_id='blue_minus_10', row=3)
    async def blue_minus_10(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.mode == 'primary':
            self.primary[2] -= 10

        if self.mode == 'secondary':
            self.secondary[2] -= 10

        pfp_response = requests.get(interaction.user.avatar.url)
        pfp_path = "pfp.png"
        with open(pfp_path, "wb") as f: f.write(pfp_response.content)
        primary, secondary = tuple(self.primary), tuple(self.secondary)
        image = create_rank_image(99, str(interaction.user.name)+'#'+str(interaction.user.discriminator), interaction.user.id, interaction.guild.id, 0.5, primary, secondary, pfp_path)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(buffer, filename="rank.png")
        embed = discord.Embed(color=0x89CFF0, description="Use the buttons below to edit the respective color values. Keep in mind the rank bar below is only an example; you must click `save` to save the colors to your profile.")
        embed.set_image(url="attachment://rank.png")
        await interaction.response.edit_message(embed=embed, attachments=[file], view=ColorButtons(self.mode, self.primary, self.secondary))

    @discord.ui.button(label='-1', style=discord.ButtonStyle.blurple, custom_id='blue_minus_1', row=3)
    async def blue_minus_1(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.mode == 'primary':
            self.primary[2] -= 1

        if self.mode == 'secondary':
            self.secondary[2] -= 1

        pfp_response = requests.get(interaction.user.avatar.url)
        pfp_path = "pfp.png"
        with open(pfp_path, "wb") as f: f.write(pfp_response.content)
        primary, secondary = tuple(self.primary), tuple(self.secondary)
        image = create_rank_image(99, str(interaction.user.name)+'#'+str(interaction.user.discriminator), interaction.user.id, interaction.guild.id, 0.5, primary, secondary, pfp_path)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(buffer, filename="rank.png")
        embed = discord.Embed(color=0x89CFF0, description="Use the buttons below to edit the respective color values. Keep in mind the rank bar below is only an example; you must click `save` to save the colors to your profile.")
        embed.set_image(url="attachment://rank.png")
        await interaction.response.edit_message(embed=embed, attachments=[file], view=ColorButtons(self.mode, self.primary, self.secondary))

    @discord.ui.button(label='ㅤ', style=discord.ButtonStyle.blurple, custom_id='blue_middle', disabled=True, row=3)
    async def blue_middle(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label='+1', style=discord.ButtonStyle.blurple, custom_id='blue_plus_1', row=3)
    async def blue_plus_1(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.mode == 'primary':
            self.primary[2] += 1

        if self.mode == 'secondary':
            self.secondary[2] += 1

        pfp_response = requests.get(interaction.user.avatar.url)
        pfp_path = "pfp.png"
        with open(pfp_path, "wb") as f: f.write(pfp_response.content)
        primary, secondary = tuple(self.primary), tuple(self.secondary)
        image = create_rank_image(99, str(interaction.user.name)+'#'+str(interaction.user.discriminator), interaction.user.id, interaction.guild.id, 0.5, primary, secondary, pfp_path)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(buffer, filename="rank.png")
        embed = discord.Embed(color=0x89CFF0, description="Use the buttons below to edit the respective color values. Keep in mind the rank bar below is only an example; you must click `save` to save the colors to your profile.")
        embed.set_image(url="attachment://rank.png")
        await interaction.response.edit_message(embed=embed, attachments=[file], view=ColorButtons(self.mode, self.primary, self.secondary))

    @discord.ui.button(label='+10', style=discord.ButtonStyle.blurple, custom_id='blue_plus_10', row=3)
    async def blue_plus_10(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.mode == 'primary':
            self.primary[2] += 10

        if self.mode == 'secondary':
            self.secondary[2] += 10


        pfp_response = requests.get(interaction.user.avatar.url)
        pfp_path = "pfp.png"
        with open(pfp_path, "wb") as f: f.write(pfp_response.content)
        primary, secondary = tuple(self.primary), tuple(self.secondary)
        image = create_rank_image(99, str(interaction.user.name)+'#'+str(interaction.user.discriminator), interaction.user.id, interaction.guild.id, 0.5, primary, secondary, pfp_path)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(buffer, filename="rank.png")
        embed = discord.Embed(color=0x89CFF0, description="Use the buttons below to edit the respective color values. Keep in mind the rank bar below is only an example; you must click `save` to save the colors to your profile.")
        embed.set_image(url="attachment://rank.png")
        await interaction.response.edit_message(embed=embed, attachments=[file], view=ColorButtons(self.mode, self.primary, self.secondary))

class Profile(commands.GroupCog, group_name='profile'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.checkpoints = [1, 10, 15, 22, 31, 42, 55, 70, 87, 106, 127, 150, 175, 202, 231, 262, 295, 330, 367, 406, 447, 490, 535, 582, 631, 682, 735, 790, 847, 906, 967, 1030, 1095, 1162, 1231, 1302, 1375, 1450, 1527, 1606, 1687, 1770, 1855, 1942, 2031, 2122, 2215, 2310, 2407, 2506, 2607, 2710, 2815, 2922, 3031, 3142, 3255, 3370, 3487, 3606, 3727, 3850, 3975, 4102, 4231, 4362, 4495, 4630, 4767, 4906, 5047, 5190, 5335, 5482, 5631, 5782, 5935, 6090, 6247, 6406, 6567, 6730, 6895, 7062, 7231, 7402, 7575, 7750, 7927, 8106, 8287, 8470, 8655, 8842, 9031, 9222, 9415, 9610, 9807, 10006, 10207]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return 
        score = get_rank_score(message.guild.id, message.author.id)
        if score:
            add_rank_score(message.guild.id, message.author.id)
        else:
            add_user(message.guild.id, message.author.id)
            add_rank_score(message.guild.id, message.author.id)

        if score in self.checkpoints:
            for i in range(len(self.checkpoints)):
                if self.checkpoints[i] <= score <= self.checkpoints[i + 1]:
                    level = i + 1

            embed = discord.Embed(color=0x89CFF0, description=f"Congratulations <@{message.author.id}>! You have reached level **{level}**! :tada:")
            await message.channel.send(embed=embed)
            await self.bot.process_commands(message)

    @app_commands.command(name='view', description='Displays your current rank.')
    async def view(self, interaction: discord.Interaction, user: discord.User=None):
        if not user: user = interaction.user

        score = get_rank_score(interaction.guild.id, user.id)
        if score is None and user != interaction.user:
            embed = discord.Embed(color=0x89CFF0, description=f"<@{user.id}> does not have logged XP. Send some messages first!")
            return await interaction.response.send_message(embed=embed)
        
        elif score is None and user == interaction.user:
            embed = discord.Embed(color=0x89CFF0, description=f"You do not have logged XP. Send some messages first!")
            return await interaction.response.send_message(embed=embed)
        
        level = 0
        progress = 0.0
        for i in range(len(self.checkpoints) - 1):
            if self.checkpoints[i] <= score < self.checkpoints[i + 1]:
                progress = (score - self.checkpoints[i]) / (self.checkpoints[i + 1] - self.checkpoints[i])
                level = i + 1
                break

        pfp_url = user.avatar.url
        pfp_response = requests.get(pfp_url)
        pfp_path = "pfp.png"
        with open(pfp_path, "wb") as f:
            f.write(pfp_response.content)

        primary, secondary = get_profile_colors(interaction.guild.id, user.id)
        
        image = create_rank_image(level, str(user.name)+'#'+str(user.discriminator), user.id, interaction.guild.id, progress, primary, secondary, pfp_path)

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        file = discord.File(buffer, filename="rank.png")
        await interaction.response.send_message(file=file)
        os.remove(pfp_path)

    @app_commands.command(name='customize', description='Updates your current profile.')
    async def customize(self, interaction: discord.Interaction):
        primary, secondary = get_profile_colors(interaction.guild.id, interaction.user.id)
        embed = discord.Embed(color=0x89CFF0, description='Use the buttons below to edit the respective color values. Keep in mind the rank bar below is only an example; you must click `save` to save the colors to your profile.')
        await interaction.response.send_message(embed=embed, view=ColorButtons('primary', list(primary), list(secondary)), ephemeral=True)


    @app_commands.command(name='leaderboard', description=' Shows the top users on the server based on xp.')
    async def leaderboard(self, interaction: discord.Interaction): #DOES NOT WORK
        top_10_users = collection.find().sort("score", pymongo.DESCENDING).limit(10)
        
        scores = ""
        for user in top_10_users:
            user_id = user['user_id']
            score = user['score']

            pos = get_user_rank_position(user_id, interaction.guild.id)
            badge = ':first_place: ' if pos == 1 else ':second_place: ' if pos == 2 else ':third_place: ' if pos == 3 else None

            scores += f"{badge}<@{user_id}>:                     {score*100}K XP\n"


        embed = discord.Embed(title="Top 10 Users by XP", color=0x89CFF0, description=scores)
        await interaction.response.send_message(embed=embed)



class Economy(commands.GroupCog, group_name='eco'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.emoji = [":gem:", ":first_place:", ":100:", ":dollar:", ":moneybag:", ":bell:"]
        print(f'Class {self.__class__.__name__} loaded.')

    #WORK, TRADE, ROB, HUNT


    @app_commands.command(name="balance", description="View your balance.")
    async def balance(self, interaction: discord.Interaction, user:discord.User=None):
        if user is None:
            user = interaction.user
            
        balance = get_economy_balance(interaction.guild.id, user.id)

        embedVar = discord.Embed(color=0xEAAA00, title=f"{user.display_name}#{user.discriminator}'s Balance:",description=f"""Wallet Balance: 💸`{balance}""")
        embedVar.set_footer(text=f'{interaction.user.display_name}#{interaction.user.discriminator}', icon_url=interaction.user.display_avatar.url)
        return await interaction.response.send_message(embed=embedVar, ephemeral=True)
   



    @app_commands.command(name="slots", description="Gamble your coins off with slot commands.")
    async def slots(self, interaction: discord.Interaction):
        one, two, three = random.choice(self.emoji), random.choice(self.emoji), random.choice(self.emoji)

        embedVar = discord.Embed(color=0xEAAA00)
        embedVar.add_field(name="Slot Machine!", value=f"<a:slot:1084337026586914857>|<a:slot:1084337026586914857>|<a:slot:1084337026586914857>")
        await interaction.response.send_message(embed=embedVar, ephemeral=True)
        time.sleep(1.5)

        embedVar = discord.Embed(color=0xEAAA00)
        embedVar.add_field(name="Slot Machine!", value=f"{one}|<a:slot:1084337026586914857>|<a:slot:1084337026586914857>")
        await interaction.edit_original_response(embed=embedVar)
        time.sleep(1.5)

        embedVar = discord.Embed(color=0xEAAA00)
        embedVar.add_field(name="Slot Machine!", value=f"{one}|{two}|<a:slot:1084337026586914857>")
        await interaction.edit_original_response(embed=embedVar)
        time.sleep(1.5)


        embedVar = discord.Embed(color=0xEAAA00)
        if one == two == three:
            profit = random.randint(100, 250)
            configure_economy_balance(interaction.guild.id, interaction.user.id, profit)
            
            embedVar.add_field(name="Jackpot!", value=f"{one}|{two}|{three}")
            embedVar.add_field(name="New Balance:", value=f"💸`{get_economy_balance(interaction.guild.id, interaction.user.id)} (+{profit})`", inline=False)
            return await interaction.edit_original_response(embed=embedVar)

        elif one == two or one == three or two == three:
            profit = random.randint(20, 37)
            configure_economy_balance(interaction.guild.id, interaction.user.id, profit)

            embedVar.add_field(name="Close!", value=f"{one}|{two}|{three}")
            embedVar.add_field(name="New Balance:", value=f"💸`{get_economy_balance(interaction.guild.id, interaction.user.id)} (+{profit})`", inline=False)
            return await interaction.edit_original_response(embed=embedVar)

        else:
            profit = random.randint(-10, 5)
            sign = '+' if profit > 0 else ''
            configure_economy_balance(interaction.guild.id, interaction.user.id, profit)

            embedVar.add_field(name="Nice Try!", value=f"{one}|{two}|{three}")
            embedVar.add_field(name="New Balance:", value=f"💸`{get_economy_balance(interaction.guild.id, interaction.user.id)} ({sign}{profit})`", inline=False)
            return await interaction.edit_original_response(embed=embedVar)   
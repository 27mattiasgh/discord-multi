import time
import json
import discord
import traceback
from discord import app_commands
from discord.ext import commands
from discord import ui
from discord.utils import get
from discord.ui import RoleSelect, ChannelSelect

class CreateTicketButtons(discord.ui.View):
    def __init__(self, guild_id, is_public=None):
        super().__init__(timeout=180)

        with open(r'settings\data.json', 'r') as f:
            self.data = json.load(f) 

        if is_public is not None:
            if is_public:
                self.data['tickets']['is_public'] = True
                self.public_or_private.label = "Public"
                self.public_or_private.style = discord.ButtonStyle.green

            if not is_public:
                self.data['tickets']['is_public'] = False
                self.public_or_private.label = "Private"
                self.public_or_private.style = discord.ButtonStyle.red

            with open(r'settings\data.json', 'w') as f:
                json.dump(self.data, f)

        self.guild_id = guild_id


        if self.data['tickets']['channel'] is not None:
            self.channel.style = discord.ButtonStyle.green

        if self.data['tickets']['description'] is not None:
            self.description.style = discord.ButtonStyle.green

        if self.data['tickets']['role'] is not None:
            self.role.style = discord.ButtonStyle.green

        if self.data['tickets']['channel'] is not None and self.data['tickets']['description'] is not None and self.data['tickets']['role'] is not None and self.data['tickets']['is_public'] is not None:
            self.create.disabled = False
        else:
            self.create.disabled = True

    @discord.ui.button(label="Support Channel", custom_id='channel', style=discord.ButtonStyle.grey)
    async def channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(color=0x89CFF0, description="Select the support channel using the drop-down below:")
        await interaction.response.edit_message(embed=embed, view=ChannelSelection()) 

    @discord.ui.button(label="Support Role", custom_id='role', style=discord.ButtonStyle.grey)
    async def role(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(color=0x89CFF0, description="Select the support role using the drop-down below:")
        await interaction.response.edit_message(embed=embed, view=RoleSelection()) 

    @discord.ui.button(label="Description", custom_id='description', style=discord.ButtonStyle.grey)
    async def description(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TicketDescriptionModal())

    @discord.ui.button(label="Public/Private", custom_id='public_or_private', style=discord.ButtonStyle.grey)
    async def public_or_private(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open(r'settings\data.json', 'r') as f:
            data = json.load(f)

        if self.data['tickets']['is_public'] == True:
            is_public = False #if public

        if self.data['tickets']['is_public'] == False or self.data['tickets']['is_public'] is None:
            is_public = True #if blank or not public

        description = f"""{data['tickets']['description']}""" if data['tickets']['description'] else 'None'
        channel = f"""<#{data['tickets']['channel']}>""" if data['tickets']['channel'] else 'None'
        role = f"""<@&{data['tickets']['role']}>""" if data['tickets']['role'] else 'None'
        embed = discord.Embed(color=0x89CFF0, title='Support Ticket Panel Creator', description=f"Press buttons below to create the support ticket panel.\n\n**Channel:** {channel}\n\n**Support Role:** {role}\n\n**Description:** {description}")
        await interaction.response.edit_message(embed=embed, view=CreateTicketButtons(interaction.guild.id, is_public=is_public))
        

    @discord.ui.button(label="Create", custom_id='create', style=discord.ButtonStyle.blurple, disabled=True)
    async def create(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open(r'settings\data.json', 'r') as f:
            data = json.load(f)        

        channel = interaction.guild.get_channel(int(data['tickets']['channel']))
        embed = discord.Embed(color=0x89CFF0, description=f"{data['tickets']['description']}\n")
        msg = await channel.send(embed=embed, view=TicketButtons())

        embed = discord.Embed(color=0x89CFF0, description=f"[Ticket Panel Created!]({msg.jump_url})")
        return await interaction.response.edit_message(embed=embed, delete_after=10, view=None)    
class ChannelSelection(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=45)

    @ui.select(cls=ChannelSelect, placeholder="Select a Channel",min_values=1, max_values=1)
    async def select_callback(self, interaction:discord.Interaction, select):

        with open(r'settings\data.json', 'r') as f:
            data = json.load(f)

        channel = discord.utils.get(interaction.guild.text_channels, name=str(select.values[0]))
        data['tickets']['channel'] = str(channel.id)

        with open(r'settings\data.json', 'w') as f:
            json.dump(data, f)
    
        description = f"""{data['tickets']['description']}""" if data['tickets']['description'] else 'None'
        channel = f"""<#{data['tickets']['channel']}>""" if data['tickets']['channel'] else 'None'
        role = f"""<@&{data['tickets']['role']}>""" if data['tickets']['role'] else 'None'
        embed = discord.Embed(color=0x89CFF0, title='Support Ticket Panel Creator', description=f"Press buttons below to create the support ticket panel.\n\n**Channel:** {channel}\n\n**Support Role:** {role}\n\n**Description:** {description}")
        await interaction.response.edit_message(embed=embed, view=CreateTicketButtons(interaction.guild.id, is_public=data['tickets']['is_public']))
class RoleSelection(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=45)

    @ui.select(cls=RoleSelect, placeholder="Select a Role", min_values=1, max_values=1)
    async def select_callback(self, interaction:discord.Interaction, select):

        with open(r'settings\data.json', 'r') as f:
            data = json.load(f)

        role = discord.utils.get(interaction.guild.roles, name=str(select.values[0]))
        data['tickets']['role'] = str(role.id)

        with open(r'settings\data.json', 'w') as f:
            json.dump(data, f)
    
        description = f"""{data['tickets']['description']}""" if data['tickets']['description'] else 'None'
        channel = f"""<#{data['tickets']['channel']}>""" if data['tickets']['channel'] else 'None'
        role = f"""<@&{data['tickets']['role']}>""" if data['tickets']['role'] else 'None'
        embed = discord.Embed(color=0x89CFF0, title='Support Ticket Panel Creator', description=f"Press buttons below to create the support ticket panel.\n\n**Channel:** {channel}\n\n**Support Role:** {role}\n\n**Description:** {description}")
        await interaction.response.edit_message(embed=embed, view=CreateTicketButtons(interaction.guild.id, is_public=data['tickets']['is_public']))
class TicketDescriptionModal(discord.ui.Modal, title='Support Ticket Panel Description'):
    body = ui.TextInput(label='Enter Your Description:', style=discord.TextStyle.long, placeholder='Type Here',  max_length=2000)
    async def on_submit(self, interaction: discord.Interaction):
        with open(r'settings\data.json', 'r') as f:
            data = json.load(f)
        data['tickets']['description'] = self.body.value
        with open(r'settings\data.json', 'w') as f:
            json.dump(data, f)

        description = f"""{data['tickets']['description']}""" if data['tickets']['description'] else 'None'
        channel = f"""<#{data['tickets']['channel']}>""" if data['tickets']['channel'] else 'None'
        role = f"""<@&{data['tickets']['role']}>""" if data['tickets']['role'] else 'None'
        embed = discord.Embed(color=0x89CFF0, title='Support Ticket Panel Creator', description=f"Press buttons below to create the support ticket panel.\n\n**Channel:** {channel}\n\n**Support Role:** {role}\n\n**Description:** {description}")
        await interaction.response.edit_message(embed=embed, view=CreateTicketButtons(interaction.guild.id, is_public=data['tickets']['is_public']))
class TicketButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Ticket', style=discord.ButtonStyle.green, custom_id='create_ticket')
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TicketModal())
class TicketCloseButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Close', style=discord.ButtonStyle.red, custom_id='close_ticket')
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(color=0x89CFF0, description=f"Thread Closing!")
        embed.set_footer(text=f'Triggered by {interaction.user}', icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)
        time.sleep(3)
        return await interaction.channel.delete()
class TicketModal(discord.ui.Modal, title='Support Ticket'):

    title_body = discord.ui.TextInput(label='Title', placeholder='Type Here...', max_length=256)
    description_body = discord.ui.TextInput(label='Describe Your Issue:', style=discord.TextStyle.long, placeholder='Type Here...', max_length=2500,)
    
    async def on_submit(self, interaction: discord.Interaction):
        with open(r'settings\data.json', 'r') as f:
            data = json.load(f)

        thread = await interaction.channel.create_thread(name=f'{interaction.user} Support Thread', auto_archive_duration=1440, type=discord.ChannelType.private_thread if data['tickets']['is_public'] == False else discord.ChannelType.public_thread)
        embed = discord.Embed(color=0x89CFF0, title=self.title_body.value, description=f"{self.description_body.value}\n\n**Some Things To Note:**\n• Mentioning a user automatically adds them to this thread.\n• Once done, anyone can click the close button below to delete the thread.")
        embed.set_footer(text=f'Requested by {interaction.user}', icon_url=interaction.user.display_avatar.url)
        msg = await thread.send(embed=embed, view=TicketCloseButtons())

        await thread.add_user(interaction.user)
        await msg.pin()
        embed = discord.Embed(color=0x89CFF0, description=f'Your support thread has been created. <#{thread.id}>')
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=25)

        try: 
            role = get(interaction.guild.roles, id=int(data['tickets']['role']))
            await thread.send(f'<@{role.id}>', delete_after=1)
        except Exception as e: print(e)
    

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Something went wrong.', ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)
class Ticket(commands.GroupCog, group_name='ticket'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print(f'Class {self.__class__.__name__} loaded.')

    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.command(name='create', description='Create a new ticket panel. Should only be run by moderators.')
    async def create(self, interaction: discord.Interaction):
        with open(r'settings\data.json', 'r') as f:

            data = json.load(f)

        data['tickets']['description'] = None
        data['tickets']['channel'] = None
        data['tickets']['role'] = None
        data['tickets']['is_public'] = None
        with open(r'settings\data.json', 'w') as f:
            json.dump(data, f)

        description = f"""{data['tickets']['description']}""" if data['tickets']['description'] else 'None'
        channel = f"""<#{data['tickets']['channel']}>""" if data['tickets']['channel'] else 'None'
        role = f"""<@&{data['tickets']['role']}>""" if data['tickets']['role'] else 'None'
        print(description, channel, role)

        embed = discord.Embed(color=0x89CFF0, title='Support Ticket Panel Creator', description=f"Press buttons below to create the support ticket panel.\n\n**Channel:** {channel}\n\n**Support Role:** {role}\n\n**Description:** {description}")
        await interaction.response.send_message(embed=embed, view=CreateTicketButtons(interaction.guild.id), ephemeral=True)


class PollButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Vote!', style=discord.ButtonStyle.green, custom_id='vote')
    async def vote(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(color=0x89CFF0, description="Select your prefrence using the drop-down menu below:")
        await interaction.response.edit_message(embed=embed, view=PollChannelSelection()) 

    @discord.ui.button(label='Close', style=discord.ButtonStyle.red, custom_id='close')
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(PollModal())


class PollChannelSelection(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=45)

    @ui.select(placeholder="Select Your Prefrence",min_values=1, max_values=1)
    async def select_callback(self, interaction:discord.Interaction, select):
        choice = select.values[0]

        

        




class PollCreateButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Channel', style=discord.ButtonStyle.grey, custom_id='channels')
    async def channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(color=0x89CFF0, description="Select the poll channel using the drop-down below:")
        await interaction.response.edit_message(embed=embed, view=PollChannelSelection()) 

    @discord.ui.button(label='Description', style=discord.ButtonStyle.grey, custom_id='description')
    async def description(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(PollModal())

    @discord.ui.button(label='Create', style=discord.ButtonStyle.grey, custom_id='create')
    async def create(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open(r'settings\data.json', 'r') as f:data = json.load(f)        
        channel = interaction.guild.get_channel(int(data['poll']['channel']))
        options = "\n".join(data['poll']['options'])
        embed = discord.Embed(color=0x89CFF0, title=f"New Poll: {data['poll']['title'].title()}",description=f"""**{data['poll']['description']}**\n\nOptions: **{options}**""")
        await channel.send(embed=embed)


class PollModal(discord.ui.Modal, title='Poll Value Editor'):
    title_body = discord.ui.TextInput(label='Title', placeholder='Type Here...', max_length=256)
    description = ui.TextInput(label='Enter Poll Description:', style=discord.TextStyle.long, placeholder='Type Description Here',  max_length=2000)
    options = ui.TextInput(label='Enter Poll Options:', style=discord.TextStyle.long, placeholder='Enter your options without commas or periods, but include spaces.\n\nExample:\n\nCats Dogs Birds',  max_length=2000)
    async def on_submit(self, interaction: discord.Interaction):
        with open(r'settings\data.json', 'r') as f:data = json.load(f)
        data['poll']['title'] = self.title_body.value
        data['poll']['description'] = self.description.value
        data['poll']['options'] = self.options.value.split()
        with open(r'settings\data.json', 'w') as f:json.dump(data, f)
        channel = f"""<#{data['poll']['channel']}>""" if data['poll']['channel'] else 'None'
        title = f"""{data['poll']['title']}""" if data['poll']['title'] else 'None'
        description = f"""{data['poll']['description']}""" if data['poll']['description'] else 'None'
        options = "\n".join(data['poll']['options']) if data['poll']['options'] else 'None'
        embed = discord.Embed(color=0x89CFF0, title='Poll Creator', description=f"Press buttons below to create the poll.\n\n**Channel:** {channel}\n\n**Title:** {title}\n\n**Description** {description}\n\n**Options:** {options}")
        await interaction.response.edit_message(embed=embed, view=PollCreateButtons())

class PollChannelSelection(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=45)
    @ui.select(cls=ChannelSelect, placeholder="Select a Channel",min_values=1, max_values=1)
    async def select_callback(self, interaction:discord.Interaction, select):
        with open(r'settings\data.json', 'r') as f:data = json.load(f)
        channel = discord.utils.get(interaction.guild.text_channels, name=str(select.values[0]))
        data['poll']['channel'] = str(channel.id)
        with open(r'settings\data.json', 'w') as f:json.dump(data, f)
        channel = f"""<#{data['poll']['channel']}>""" if data['poll']['channel'] else 'None'
        title = f"""{data['poll']['title']}""" if data['poll']['title'] else 'None'
        description = f"""{data['poll']['description']}""" if data['poll']['description'] else 'None'
        options = "\n".join(data['poll']['options']) if data['poll']['options'] else 'None'
        embed = discord.Embed(color=0x89CFF0, title='Poll Creator', description=f"Press buttons below to create the poll.\n\n**Channel:** {channel}\n\n**Title:** {title}\n\n**Description** {description}\n\n**Options:** {options}")
        await interaction.response.edit_message(embed=embed, view=PollCreateButtons())



class Poll(commands.GroupCog, group_name='poll'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print(f'Class {self.__class__.__name__} loaded.')
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.command(name='create', description='Create a new poll. Should only be run by moderators.')
    async def create(self, interaction: discord.Interaction):
        channel = 'None'
        title = 'None'
        description = 'None'
        options = 'None'
        embed = discord.Embed(color=0x89CFF0, title='Poll Creator', description=f"Press buttons below to create the poll.\n\n**Channel:** {channel}\n\n**Title:** {title}\n\n**Description** {description}\n\n**Options:** {options}")
        await interaction.response.send_message(embed=embed, view=PollCreateButtons())


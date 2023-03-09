import json
import discord
from discord import app_commands
from discord.ext import commands

#add lockdown, unban, mute/timeout

class ConfirmationButtons(discord.ui.View):
    def __init__(self, member:discord.Member, user:discord.Member, total_infractions:int, reason:str, action:str):
        super().__init__(timeout=45)
        self.user = user
        self.member = member
        print(self.member.id)
        self.total_infractions = total_infractions
        self.reason = reason
        self.action = action
        print(self.user, self.member, self.total_infractions, self.reason, self.action)

    @discord.ui.button(label="Yes",style=discord.ButtonStyle.green)
    async def confirm_yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.action == 'kick':
            dm = await self.member.create_dm()
            embedUser = discord.Embed(color=0x009a00)
            embedUser.set_author(name=f'{self.member.display_name} has been kicked.')
            await interaction.response.send_message(embed=embedUser, ephemeral=True) 
            embedMember = discord.Embed(color=0x009a00)
            embedMember.set_author(name=f'You have been kicked in {interaction.guild}. Reason: {self.reason}.')
            await dm.send(embed=embedMember)
            await self.member.kick()

        if self.action == 'ban':
            dm = await self.member.create_dm()
            embedUser = discord.Embed(color=0x009a00)
            embedUser.set_author(name=f'{self.member.display_name} has been banned.')
            await interaction.response.send_message(embed=embedUser, ephemeral=True) 
            embedMember = discord.Embed(color=0x009a00)
            embedMember.set_author(name=f'You have been banned in {interaction.guild}. Reason: {self.reason}.')
            await dm.send(embed=embedMember)
            await self.member.ban()

    @discord.ui.button(label="No",style=discord.ButtonStyle.red)
    async def confirm_no(self, interaction: discord.Interaction, button: discord.ui.Button):
        embedVar = discord.Embed(color=0xCF142B)
        embedVar.set_author(name=f'Ok, action canceled.')  
        return await interaction.response.edit_message(embed=embedVar)

class MoreInfoButtons(discord.ui.View):
    def __init__(self, member:discord.Member, user:discord.Member, total_infractions:int):
        super().__init__(timeout=30)
        self.user = user
        self.member = member
        self.total_infractions = total_infractions

    @discord.ui.button(label="View More Information", custom_id='view_more_information', style=discord.ButtonStyle.green)
    async def view_more_information(self, interaction: discord.Interaction, button: discord.ui.Button):
        embedVar = discord.Embed(color=0x009a00)
        embedVar.add_field(name='Performed by:', value=f'<@{self.user.id}>', inline=False)
        embedVar.add_field(name='Performed in:', value=f'<#{interaction.channel_id}>', inline=False)        
        embedVar.add_field(name='Total Infractions:', value=self.total_infractions, inline=False) 
        embedVar.add_field(name='AutoModeration:', value='False', inline=False) 

        self.view_more_information.disabled = True
        return await interaction.response.edit_message(embed=embedVar, view=self)


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.command(name="warn", description="warn a user")
    async def warn(self, interaction: discord.Interaction, member:discord.User, reason:str):
        user = interaction.user

        with open(r'C:\Users\Mati\OneDrive\Desktop\Discord Slash Commands\json data\infractions.json') as f:
            data = json.load(f)
        data[str(member.id)] += 1
        total_infractions = data[str(member.id)]
        with open(r'C:\Users\Mati\OneDrive\Desktop\Discord Slash Commands\json data\infractions.json', 'w') as f:
            json.dump(data, f)

        dm = await member.create_dm()
        embedMember = discord.Embed(color=0x009a00)
        embedMember.set_author(name=f'You have been warned in {interaction.guild} due to {reason}.')
        await dm.send(embed=embedMember, view=MoreInfoButtons(member, user, total_infractions))
        embedUser = discord.Embed(color=0x009a00)
        embedUser.set_author(name=f'{member.display_name} has been warned.')
        await interaction.response.send_message(embed=embedUser, ephemeral=True)


    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.command(name="kick", description="kick a user")
    async def kick(self, interaction: discord.Interaction, member:discord.User, reason:str):
        user = interaction.user
        with open(r'C:\Users\Mati\OneDrive\Desktop\Discord Slash Commands\json data\infractions.json') as f:
            data = json.load(f)
        total_infractions = data[str(member.id)]
        if total_infractions == 0:
            action = 'kick'
            embedVar = discord.Embed(color=0x009a00)
            embedVar.set_author(name=f'This user has no active infractions. Are you sure you want to perform this opperation?')  
            return await interaction.response.send_message(embed=embedVar, view=ConfirmationButtons(member, user, total_infractions, reason, action), ephemeral=True)

        dm = await member.create_dm()
        embedMember = discord.Embed(color=0x009a00)
        embedMember.set_author(name=f'You have been kicked in {interaction.guild}. Reason: {reason}.')
        await dm.send(embed=embedMember, view=MoreInfoButtons(member, user, total_infractions))
        await member.kick()
        embedUser = discord.Embed(color=0x009a00)
        embedUser.set_author(name=f'{member.display_name} has been kicked.')
        await interaction.response.send_message(embed=embedUser, ephemeral=True) 



    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.command(name="ban", description="ban a user")
    async def ban(self, interaction: discord.Interaction, member:discord.User, reason:str):
        user = interaction.user
        with open(r'C:\Users\Mati\OneDrive\Desktop\Discord Slash Commands\json data\infractions.json') as f:
            data = json.load(f)
        total_infractions = data[str(member.id)]
        if total_infractions == 0:
            action = 'ban'
            embedVar = discord.Embed(color=0x009a00)
            embedVar.set_author(name=f'This user has no active infractions. Are you sure you want to perform this opperation?')  
            return await interaction.response.send_message(embed=embedVar, view=ConfirmationButtons(member, user, total_infractions, reason, action), ephemeral=True)

        dm = await member.create_dm()
        embedMember = discord.Embed(color=0x009a00)
        embedMember.set_author(name=f'You have been banned in {interaction.guild}. Reason: {reason}.')
        await dm.send(embed=embedMember, view=MoreInfoButtons(member, user, total_infractions))
        await member.ban()
        embedUser = discord.Embed(color=0x009a00)
        embedUser.set_author(name=f'{member.display_name} has been banned.')
        await interaction.response.send_message(embed=embedUser, ephemeral=True) 



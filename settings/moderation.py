import json
import discord
from discord import app_commands
from discord.ext import commands

class MoreInfoButtons(discord.ui.View):
    def __init__(self, member:discord.Member, user:discord.Member):
        super().__init__(timeout=30)
        self.user = user
        self.member = member

    @discord.ui.button(label="View More Information", custom_id='view_more_information', style=discord.ButtonStyle.green)
    async def view_more_information(self, interaction: discord.Interaction, button: discord.ui.Button):
        embedVar = discord.Embed(color=0x009a00)
        embedVar.add_field(name='Performed by:', value=f'<@{self.user.id}>', inline=False)
        embedVar.add_field(name='Performed in:', value=f'<#{interaction.channel_id}>', inline=False)        
        embedVar.add_field(name='AutoModeration:', value='False', inline=False) 

        self.view_more_information.disabled = True
        return await interaction.response.edit_message(embed=embedVar, view=self)

class Moderation(commands.GroupCog, group_name='moderation'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print(f'Class {self.__class__.__name__} loaded.')

    #Editing user permissions

    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.command(name="warn", description="Warn the specified user. Requires manage message permissions.")
    async def warn(self, interaction: discord.Interaction, target:discord.User, reason:str = None):
        reason = 'None' if reason is None else reason

        user = interaction.user

        with open(r'moderation\moderation.json') as f:
            data = json.load(f)
        data[str(target.id)] += 1
        with open(r'moderation\moderation.json', 'w') as f:
            json.dump(data, f)

        dm = await target.create_dm()
        embedMember = discord.Embed(color=0x009a00)
        embedMember.set_author(name=f'You have been warned in {interaction.guild} due to {reason}.')
        await dm.send(embed=embedMember, view=MoreInfoButtons(target, user))
        embedUser = discord.Embed(color=0x009a00)
        embedUser.set_author(name=f'{target.display_name} has been warned.')
        return await interaction.response.send_message(embed=embedUser, ephemeral=True)

    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.command(name="kick", description="Kick the specified user. Requires kick permissions.")
    async def kick(self, interaction: discord.Interaction, target:discord.User, reason:str = None):
        reason = 'None' if reason is None else reason

        user = interaction.user
        with open(r'moderation\moderation.json') as f:
            data = json.load(f)

        dm = await target.create_dm()

        embedMember = discord.Embed(color=0x009a00)
        embedMember.set_author(name=f'You have been kicked in {interaction.guild}. Reason: {reason}.')
        await dm.send(embed=embedMember)
        await target.kick()

        embedUser = discord.Embed(color=0x009a00)
        embedUser.set_author(name=f'{target.display_name} has been kicked.')
        return await interaction.response.send_message(embed=embedUser, ephemeral=True) 

    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.command(name="ban", description="Ban the specified user. Requires ban permissions.")
    async def ban(self, interaction: discord.Interaction, target:discord.User, reason:str = None):
        if target.top_role >= interaction.author.top_role:
            return await interaction.response.send_message("You can only ban people below you.")

        reason = 'None' if reason is None else reason
        user = interaction.user

        dm = await target.create_dm()
        embed = discord.Embed(color=0x009a00, description=f'You have been banned in {interaction.guild}. Reason: {reason}')
        await dm.send(embed=embed, view=MoreInfoButtons(target, user))
        await target.ban()
        
        embed = discord.Embed(color=0x009a00, description=f'<@{target.id}> has been banned.')
        return await interaction.response.send_message(embed=embed, ephemeral=True) 
    
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.command(name="unban", description="Unban the specified user. Requires the user's ID. Requires ban permissions.")
    async def unban(self, interaction: discord.Interaction, id:int):
        user = await self.bot.fetch_user(id)
        await user.unban()
        
        embed = discord.Embed(color=0x009a00, description=f'<@{user}> has been banned.')
        return await interaction.response.send_message(embed=embed, ephemeral=True) 



    #Users, and messages

    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.command(name="lock", description="Locks a specific channel. To unlock, run this command again.")
    async def lock(self, interaction: discord.Interaction, channel:discord.TextChannel=None):

        #Get permissions for the channel to unlock/lock it
        if channel is None:
            channel = interaction.channel
            
        channel = interaction.guild.get_channel(channel.id)

        embed = discord.Embed(color=0x009a00, description=f'This channel is locked. Wait for moderators to unlock it.')
        await channel.set_permissions(interaction.guild.default_role, send_messages=False)
        await channel.send(embed=embed)

        embed = discord.Embed(color=0x009a00, description=f'<#{channel.id}> has been locked.')
        return await interaction.response.send_message(embed=embed, ephemeral=True) 

    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.command(name="lockdown", description="Locks down every channel. If you only want to lock down one, run /lock.")
    async def lockdown(self, interaction: discord.Interaction, unlock:bool):
        if not unlock:
            embed = discord.Embed(color=0x009a00, description=f'This channel is locked. Wait for moderators to unlock it.')
            for channel in interaction.guild.text_channels:
                try:
                    await channel.set_permissions(interaction.guild.default_role, send_messages=False)
                    await channel.send(embed=embed)
                except:pass

            embed = discord.Embed(color=0x009a00, description=f'Every channel has been locked. Run this command to unlock.')
            return await interaction.response.send_message(embed=embed, ephemeral=True) 
        

        else:
            for channel in interaction.guild.text_channels:
                try:
                    await channel.set_permissions(interaction.guild.default_role, send_messages=True)
                except:pass

            embed = discord.Embed(color=0x009a00, description=f'Every channel has been unlocked. Run this command to lock.')
            return await interaction.response.send_message(embed=embed, ephemeral=True) 
        
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.command(name="slowmode", description="Changes slowmode settings for the specified channel.")
    async def slowmode(self, interaction: discord.Interaction, channel:discord.TextChannel, seconds:int):

        if channel is None:
            channel = interaction.channel
        channel = interaction.guild.get_channel(channel.id)


        await channel.edit(slowmode_delay=seconds)

        word = 'seconds' if seconds > 1 else 'second'
        embed = discord.Embed(color=0x009a00, description=f'<#{channel.id}> slowmode has been set to {seconds} {word}.')
        
        return await interaction.response.send_message(embed=embed, ephemeral=True) 
    


    
import json
import time
import random
import discord
from discord.utils import get
from discord.ext import commands
from datetime import datetime, timezone

def categorize_changes(allow_before, allow_after, deny_before, deny_after):
    if allow_before is not None and allow_after is not None and deny_before is not None and deny_after is not None:
        return 'Deny -> Allow' if allow_before > allow_after and deny_before < deny_after else 'Allow -> Deny'
    elif allow_before is None and allow_after is None:
        return 'Standard -> Deny' if deny_before > deny_after else 'Deny -> Standard'
    elif deny_before is None and deny_after is None:
        return 'Standard -> Allow' if allow_before > allow_after else 'Allow -> Standard'







class Logging(commands.GroupCog, name='logging'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print(f'Class {self.__class__.__name__} loaded.')

    #USER EDITING/UPDATING
    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        pass  

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        pass  

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        #fetch channel

        if before.nick != after.nick:
            pass #send to channel (after.name changed nick before.nick -> after.nick)

        if before.guild_avatar != after.guild_avatar:
            pass

        if before.roles != after.roles:
            pass

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        #fetch channel

        if before.username != after.username:
            pass

        if before.avatar != after.avatar:
            pass #send to channel (after.avatar changed avatar before.avatar -> after.avatar)

        if before.discriminator != after.discriminator:
            pass

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        #fetch channel

        if before.status != after.status:
            pass

        if before.activity != after.activity:
            pass #send to channel (after.avatar changed avatar before.avatar -> after.avatar)


    #MESSAGE EDITING/UPDATING
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        pass

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        async for entry in message.guild.audit_logs(limit=1,action=discord.AuditLogAction.message_delete): deleter = entry.user
        print(f"{deleter.name} deleted message by {message.author.name}")


    #ROLE EDITING/UPDATING - DONE
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        target = self.bot.get_channel(1102283810411917393)
        time = datetime.now(timezone.utc).strftime('%d/%m/%Y')
        async for entry in role.guild.audit_logs(limit=1): logs = entry
        embed = discord.Embed(color=0x78b159, title=f"Role Created", description=f"""**Role:** <@&{role.id}>\n\n**Executed By:** <@{logs.user.id}>\n\n```prolog\nRole ID: {role.id}\n\nExecutor ID: {logs.user.id}```""")
        embed.set_footer(text=f"{time} UTC")
        await target.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        target = self.bot.get_channel(1102283810411917393)
        time = datetime.now(timezone.utc).strftime('%d/%m/%Y')
        async for entry in role.guild.audit_logs(limit=1): logs = entry
        embed = discord.Embed(color=0xdd2e44, title=f"Role Deleted", description=f"""**Role:** <@&{role.id}>\n\n**Executed By:** <@{logs.user.id}>\n\n```prolog\nRole ID: {role.id}\n\nExecutor ID: {logs.user.id}```""")
        embed.set_footer(text=f"{time} UTC")
        await target.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        async for entry in after.guild.audit_logs(limit=1): logs = entry

        if before.name != after.name:
            embed = discord.Embed(color=0xfdcb58, title=f"Role Updated", description=f"""**Role:** <@&{after.id}>\n\n**Role Name:** {before.name} -> {after.name}\n\n**Executed By:** <@{logs.user.id}>\n\n```prolog\nRole ID: {after.id}\n\nExecutor ID: {logs.user.id}```""")

        elif before.color != after.color:
            embed = discord.Embed(color=0xfdcb58, title=f"Role Updated", description=f"""**Role:** <@&{after.id}>\n\n**Role Color (HEX Format):** `{before.color}` -> `{after.color}`\n\n**Executed By:** <@{logs.user.id}>\n\n```prolog\nRole ID: {after.id}\n\nExecutor ID: {logs.user.id}```""")

        elif before.position != after.position:
            embed = discord.Embed(color=0xfdcb58, title=f"Role Updated", description=f"""**Role:** <@&{after.id}>\n\n**Role Position:** {before.position} -> {after.position}\n\n**Executed By:** <@{logs.user.id}>\n\n```prolog\nRole ID: {after.id}\n\nExecutor ID: {logs.user.id}```""")

        elif before.hoist != after.hoist:
            embed = discord.Embed(color=0xfdcb58, title=f"Role Updated", description=f"""**Role:** <@&{after.id}>\n\n**Role Hoist (Display Members Separately):** {before.hoist} -> {after.hoist}\n\n**Executed By:** <@{logs.user.id}>\n\n```prolog\nRole ID: {after.id}\n\nExecutor ID: {logs.user.id}```""")


        elif before.permissions != after.permissions:
            before_permissions = set([name for name, value in before.permissions if value])
            after_permissions = set([name for name, value in after.permissions if value])
            added_permissions = after_permissions - before_permissions
            removed_permissions = before_permissions - after_permissions
            added_permissions_list = []
            removed_permissions_list = []

            if added_permissions:
                for permission in added_permissions:
                    added_permissions_list.append(' '.join(word.capitalize() for word in permission.split('_')))

            if removed_permissions:
                for permission in removed_permissions:
                    removed_permissions_list.append(' '.join(word.capitalize() for word in permission.split('_')))

            added_permissions_string = ", ".join(added_permissions_list)
            removed_permissions_string = ", ".join(removed_permissions_list)

            embed = discord.Embed(color=0xfdcb58, title=f"Role Updated", description=f"""**Role:** <@&{after.id}>\n\n**Added Permissions:** {'`' + added_permissions_string + '`' if len(added_permissions_string) > 0 else ''}\n\n**Removed Permissions:** {'`' + removed_permissions_string + '`' if len(removed_permissions_string) > 0 else ''}\n\n**Executed By:** <@{logs.user.id}>\n\n```prolog\nRole ID: {after.id}\n\nExecutor ID: {logs.user.id}```""")

        else:return 

        target_channel = self.bot.get_channel(1102283810411917393)  
        embed.set_footer(text=f"{datetime.now(timezone.utc).strftime('%d/%m/%Y')} UTC")
        await target_channel.send(embed=embed)




    #CHANNELS - DONE
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        target = self.bot.get_channel(1102283810411917393)
        time = datetime.now(timezone.utc).strftime('%d/%m/%Y')
        async for entry in channel.guild.audit_logs(limit=1): logs = entry
        embed = discord.Embed(color=0x78b159, title=f"Channel Created", description=f"""**Channel:** <#{channel.id}>\n\n**Executed By:** <@{logs.user.id}>\n\n```prolog\nChannel ID: {channel.id}\n\nExecutor ID: {logs.user.id}```""")
        embed.set_footer(text=f"{time} UTC")
        await target.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        target = self.bot.get_channel(1102283810411917393)
        async for entry in channel.guild.audit_logs(limit=1): logs = entry
        embed = discord.Embed(color=0xdd2e44, title=f"Channel Deleted", description=f"""**Channel:** <#{channel.id}>\n\n**Executed By:** <@{logs.user.id}>\n\n```prolog\nChannel ID: {channel.id}\n\nExecutor ID: {logs.user.id}```""")
        embed.set_footer(text=f"{datetime.now(timezone.utc).strftime('%d/%m/%Y')} UTC")
        await target.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        change = None
        async for entry in after.guild.audit_logs(limit=1): logs = entry

        if before.name != after.name:
            embed = discord.Embed(color=0xfdcb58, title=f"Channel Updated", description=f"""**Channel:** <#{after.id}>\n\n**Old Name:** {before.name}\n\n**New Name:** {after.name}\n\n**Executed By:** <@{logs.user.id}>\n\n```prolog\nChannel ID: {after.id}\n\nExecutor ID: {logs.user.id}```""")

        elif before.category != after.category:
            embed = discord.Embed(color=0xfdcb58, title=f"Channel Updated", description=f"""**Channel:** <#{after.id}>\n\n**Old Category:** {before.category}\n\n**New Category:** {after.category}\n\n**Executed By:** <@{logs.user.id}>\n\n```prolog\nChannel ID: {after.id}\n\nOld Category ID: {before.category.id}\n\nNew Category ID: {after.category.id}\n\nExecutor ID: {logs.user.id}```""")

        elif before.position != after.position:
            embed = discord.Embed(color=0xfdcb58, title=f"Channel Updated", description=f"""**Channel:** <#{after.id}>\n\n**Old Channel Position:** {int(before.position) + 1}\n\n**New Channel Position:** {int(after.position) + 1}\n\n**Executed By:** <@{logs.user.id}>\n\n```prolog\nChannel ID: {after.id}\n\nExecutor ID: {logs.user.id}```""")

        
        elif before.overwrites != after.overwrites:
            async for entry in after.guild.audit_logs(limit=1, action=discord.AuditLogAction.overwrite_update):
                if entry.target.id == before.id and entry.after is not None:

                    role = get(after.guild.roles, name=str(entry.extra))
                    target = entry.user


                    overwrite_before = entry.before
                    overwrite_after = entry.after
                    allow_before, allow_after, deny_before, deny_after = None, None, None, None
                    try: allow_before = overwrite_after.allow.value & ~overwrite_before.allow.value
                    except: allow_before = None
                    try: allow_after = ~overwrite_after.allow.value & overwrite_before.allow.value
                    except: allow_after = None
                    try: deny_before = overwrite_after.deny.value & ~overwrite_before.deny.value
                    except: deny_before = None
                    try: deny_after = ~overwrite_after.deny.value & overwrite_before.deny.value
                    except: deny_after = None
                    change = categorize_changes(allow_before, allow_after, deny_before, deny_after)

                    try:
                        permissions_granted = overwrite_after.allow.value & ~overwrite_before.allow.value
                        permissions_revoked = ~overwrite_after.allow.value & overwrite_before.allow.value
                        granted, revoked = None, None
                        for perm, value in discord.Permissions(permissions_granted):
                            if value: granted = perm
                        for perm, value in discord.Permissions(permissions_revoked):
                            if value: revoked = perm
                        if granted is not None:
                            permission = ' '.join(word.capitalize() for word in granted.split('_'))
                        if revoked is not None:
                           permission = ' '.join(word.capitalize() for word in revoked.split('_'))

                    except:
                        permissions_before = overwrite_after.deny.value & ~overwrite_before.deny.value
                        permissions_after = ~overwrite_after.deny.value & overwrite_before.deny.value
                        granted, revoked = None, None
                        for perm, value in discord.Permissions(permissions_before):
                            if value: granted = perm
                        for perm, value in discord.Permissions(permissions_after):
                            if value: revoked = perm
                        if permissions_before > permissions_after:
                            permission = ' '.join(word.capitalize() for word in granted.split('_'))
                        else:
                            permission = ' '.join(word.capitalize() for word in revoked.split('_'))

                    embed = discord.Embed(color=0xfdcb58, title=f"Channel Permissions Updated", description=f"""**Channel:** <#{after.id}>\n\n**Permission:** {permission} `{change}`\n\n**Role Effected:** <@&{role.id}>\n\n**Executed By:** <@{target.id}>\n\n```prolog\nChannel ID: {after.id}\n\nRole ID: {role.id}\n\nExecutor ID: {target.id}```""")
                    
        try:
            target_channel = self.bot.get_channel(1102283810411917393)  
            embed.set_footer(text=f"{datetime.now(timezone.utc).strftime('%d/%m/%Y')} UTC")
            await target_channel.send(embed=embed)
        except: pass
                    



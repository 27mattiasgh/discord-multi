import sys
import json


import discord
from discord.ext import commands
from discord.utils import get
from discord import app_commands

from economy.balance import Balance

from games.tictactoe import Tictactoe

from moderation.moderation import Moderation
from settings.config import Config
from settings.help import Help

from moderation.verification import Verification

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
synced = False

@bot.command()
async def sync(ctx: commands.Context):
    synced = True
    if ctx.message.author.id == 699679392363970580 or 655866024922447922:
        message = await ctx.send('`attempting to add cogs`')

        try:
            await bot.add_cog(Moderation(bot))


            await bot.add_cog(Verification(bot))


            await bot.add_cog(Config(bot))
            await bot.add_cog(Help(bot))

            await bot.add_cog(Tictactoe(bot))  
            await bot.add_cog(Balance(bot))

        except Exception as e:
            return await ctx.send(f'`cogs already loaded  {e}`')

        await message.edit(content='`attempting to sync`')

        await message.edit(content=f"`latency: {bot.latency}`")
        bot.tree.copy_global_to(guild=ctx.guild)
        output = await bot.tree.sync(guild=ctx.guild)
        return await message.edit(content=f"`{len(output)} cogs up`")
    await ctx.send('`incorrect permissions to execute this command`')

bot.run("MTA4MDkwNDQ5MjkzMDgzMDM2Ng.G_xijG.F8ZaUlAYUj3ZL00j1GCMkxP7z87qj6vlhPxtDs")

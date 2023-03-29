import sys

import discord
from discord.ext import commands
from discord.utils import get
from discord import app_commands


from economy.balance import Balance

from games.tictactoe import Tictactoe

from moderation.moderation import Moderation
from moderation.verification import Verification

from settings.help import Help
from settings.help import Config



intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')



@bot.command()
async def sync(ctx: commands.Context, exit=None):
    if exit is not None:
        sys.exit()

    if ctx.message.author.id == 699679392363970580 or 655866024922447922:

        try:
            await bot.add_cog(Moderation(bot))
            await bot.add_cog(Verification(bot))

            await bot.add_cog(Config(bot))
            await bot.add_cog(Help(bot))

            await bot.add_cog(Tictactoe(bot))  
            await bot.add_cog(Balance(bot))

        except Exception as e:
            embedVar = discord.Embed(color=0x89CFF0, description=f"error: `{e}`")
            return await ctx.send(embed=embedVar)


        bot.tree.copy_global_to(guild=ctx.guild)
        await bot.tree.sync(guild=ctx.guild)

        embedVar = discord.Embed(color=0x89CFF0, description="all commands loaded.")
        return await ctx.send(embed=embedVar) 
    
    embedVar = discord.Embed(color=0x89CFF0, description="incorrect permissions to perform this command.")
    return await ctx.send(embed=embedVar)

bot.run("MTA4MDkwNDQ5MjkzMDgzMDM2Ng.G_xijG.F8ZaUlAYUj3ZL00j1GCMkxP7z87qj6vlhPxtDs")

import sys

import discord
from discord.ext import commands
from discord.utils import get
from discord import app_commands


from economy.balance import Economy

from games.tictactoe import Tictactoe

from settings.moderation import Moderation
from settings.verification import Verification

from settings.help import Help
from settings.help import Config

from select_menus import Wager



intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)




@bot.command()
async def sync(ctx: commands.Context, exit=None):
    if exit == 'e' and ctx.author.id == 699679392363970580:
        sys.exit()

    try:

        #await bot.add_cog(Moderation(bot))
        await bot.add_cog(Verification(bot))

        #await bot.add_cog(Config(bot))
        await bot.add_cog(Help(bot))

        await bot.add_cog(Tictactoe(bot))  
        #await bot.add_cog(Economy(bot))


        await bot.tree.sync(guild=None)

    except Exception as e:
        embedVar = discord.Embed(color=0x89CFF0, description=f"Error: `{e}`")
        return await ctx.send(embed=embedVar, ephemeral=True)

    embedVar = discord.Embed(color=0x89CFF0, description="All commands loaded.",)
    return await ctx.send(embed=embedVar, ephemeral=True) 
    

# url ---> https://discord.com/api/oauth2/authorize?client_id=1080904492930830366&permissions=8&scope=applications.commands%20bot
bot.run("MTA4MDkwNDQ5MjkzMDgzMDM2Ng.G_xijG.F8ZaUlAYUj3ZL00j1GCMkxP7z87qj6vlhPxtDs")
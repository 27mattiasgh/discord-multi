import discord
import sys
from discord.ext import commands

from games.wager import Wager
from games.tictactoe import Tictactoe

from settings.moderation import Moderation
from settings.config import Config
from settings.help import Help



intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def sync(ctx: commands.Context):
    if ctx.message.author.id == 699679392363970580 or 655866024922447922:
        message = await ctx.send('`attempting to add cogs`')

        try:
            await bot.add_cog(Wager(bot))
            await bot.add_cog(Moderation(bot))
            await bot.add_cog(Config(bot))
            await bot.add_cog(Help(bot))
            await bot.add_cog(Tictactoe(bot))   
        except:
            return await ctx.send('`cogs already loaded`')

        await message.edit(content='`attempting to sync`')

        await message.edit(content=f"`latency: {bot.latency}`")
        bot.tree.copy_global_to(guild=ctx.guild)
        output = await bot.tree.sync(guild=ctx.guild)
        return await message.edit(content=f"`{len(output)} cogs up`")
    await ctx.send('`incorrect permissions to execute this command`')

@bot.command()
async def ping(ctx: commands.Context):
    if ctx.message.author.id == 699679392363970580 or 655866024922447922:
        return await ctx.send(f'`{bot.latency} api latency`')
    await ctx.send('`incorrect permissions to execute this command`')    

@bot.command()
async def exit(ctx: commands.Context):
    if ctx.message.author.id == 699679392363970580 or 655866024922447922:
        await ctx.send(f'`exiting program`')
        sys.exit()
    await ctx.send('`incorrect permissions to execute this command`')    

bot.run("MTA4MDkwNDQ5MjkzMDgzMDM2Ng.G_xijG.F8ZaUlAYUj3ZL00j1GCMkxP7z87qj6vlhPxtDs")

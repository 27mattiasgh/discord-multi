import sys
import discord
from discord.ext import commands



from games.games import Games

from settings.moderation import Moderation
from settings.verification import Verification
from settings.help import Help
from settings.logging import Logging
from settings.help import Config


from economy.profile import Profile
from economy.profile import Economy


from settings.tickets import Ticket
from settings.tickets import Poll

from settings.tickets import TicketButtons
from settings.tickets import TicketCloseButtons
from settings.tickets import PollButtons


class Main(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        self.add_view(TicketButtons())
        self.add_view(PollButtons())
        self.add_view(TicketCloseButtons())
        
    async def on_ready(self):
        print(f'{self.user} Up\n')
bot = Main()

@bot.command()
async def sync(ctx: commands.Context, exit=None):
    async with ctx.typing():
        if exit == 'e' and ctx.author.id == 699679392363970580:
            sys.exit()

        try:
            await bot.add_cog(Moderation(bot))
            await bot.add_cog(Verification(bot))

            await bot.add_cog(Poll(bot))

            await bot.add_cog(Profile(bot))

            await bot.add_cog(Logging(bot))

            await bot.add_cog(Ticket(bot))
            await bot.add_cog(Config(bot))
            await bot.add_cog(Help(bot))

            await bot.add_cog(Games(bot))  
            await bot.add_cog(Economy(bot))

            await bot.tree.sync(guild=None)

        except Exception as e:
            embedVar = discord.Embed(color=0x89CFF0, description=f"Error: `{e}`")
            return await ctx.send(embed=embedVar, ephemeral=True)

        embedVar = discord.Embed(color=0x89CFF0, description="All commands loaded.",)
        return await ctx.send(embed=embedVar, ephemeral=True) 
    

# joinurl ---> https://discord.com/api/oauth2/authorize?client_id=1080904492930830366&permissions=8&scope=applications.commands%20bot
bot.run("MTA4MDkwNDQ5MjkzMDgzMDM2Ng.G2Px3a.7YKVECx4fSys4WESBG0dqc-6npVL9uq6EgsaJk")
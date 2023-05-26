import json
import discord
from discord import app_commands
from discord.ext import commands

class PageinatorButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.current_page = -1

        self.embed_pages = [

            ["`/tictactoe`", "Initiates a new game of Tic Tac Toe between the player and the computer."],

            ["`/help`", "Shows a list of available commands.", 
             "`/config`", "Edits the save configuration of JSON files. Requires admin permissions."],

            ["`/kick`", "Kicks a user. Requires kick permissions.",
             "`/ban`", "Bans a user. Requires ban permissions.",
             "`/warn`", "Warns a user. Requires kick permissions."],

            ["`/ticket create`", "Create a new poll. Should only be run by moderators."],
        ]


        self.max = len(self.embed_pages) - 1
        self.min = 0
        max = len(self.embed_pages)


        self.embed_first_name = f'Page {self.min} Title'
        self.embed_first_value = f'Page {self.min} Value'


        self.embed_last_name = f'Page {self.max} Title'
        self.embed_last_value = f'Page {self.max} Value'
            
        
    @discord.ui.button(label="|<", custom_id='left_home', style=discord.ButtonStyle.blurple, row=0, disabled=True)
    async def left_home(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = self.min
        embedVar = discord.Embed(color=0x89CFF0)
        
        self.left_button.disabled = True
        self.left_home.disabled = True
        self.right_button.disabled = False
        self.right_home.disabled = False
        self.page_number.label = f"{self.current_page + 1}/{self.max + 1}"

        x = self.embed_pages[self.min] 
        for i in range(0, len(x), 2):
            embedVar.add_field(name=x[i], value=x[i + 1], inline=False)

        await interaction.response.edit_message(embed=embedVar, view=self)

    @discord.ui.button(label="<", custom_id='left_button', style=discord.ButtonStyle.grey, row=0, disabled=True)
    async def left_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page != self.min:
            self.current_page -= 1

        embedVar = discord.Embed(color=0x89CFF0)
        if self.current_page == self.min:
            self.left_button.disabled = True
            self.left_home.disabled = True
            self.right_button.disabled = False
            self.right_home.disabled = False
            self.page_number.label = f"{self.current_page + 1}/{self.max + 1}"

            x = self.embed_pages[self.current_page] 
            for i in range(0, len(x), 2):
                embedVar.add_field(name=x[i], value=x[i + 1], inline=False)

        else:
            self.left_button.disabled = False
            self.right_button.disabled = False
            self.left_home.disabled = False
            self.right_home.disabled = False
            self.page_number.label = f"{self.current_page + 1}/{self.max + 1}"

            x = self.embed_pages[self.current_page] 
            for i in range(0, len(x), 2):
                embedVar.add_field(name=x[i], value=x[i + 1], inline=False)

        await interaction.response.edit_message(embed=embedVar, view=self)

    @discord.ui.button(label=f"Menu", custom_id='page_number', style=discord.ButtonStyle.green, row=0, disabled=True)
    async def page_number(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label=">", custom_id='right_button', style=discord.ButtonStyle.grey, row=0)
    async def right_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page != self.max:
            self.current_page += 1
        
        embedVar = discord.Embed(color=0x89CFF0)
        if self.current_page == self.max:
            self.right_button.disabled = True
            self.right_home.disabled = True
            self.left_button.disabled = False
            self.left_home.disabled = False
            self.page_number.label = f"{self.current_page + 1}/{self.max + 1}"

            x = self.embed_pages[self.current_page] 
            for i in range(0, len(x), 2):
                embedVar.add_field(name=x[i], value=x[i + 1], inline=False)

        else:
            self.left_button.disabled = False
            self.right_button.disabled = False
            self.left_home.disabled = False
            self.right_home.disabled = False
            self.page_number.label = f"{self.current_page + 1}/{self.max + 1}"

            x = self.embed_pages[self.current_page] 
            for i in range(0, len(x), 2):
                embedVar.add_field(name=x[i], value=x[i + 1], inline=False)

        await interaction.response.edit_message(embed=embedVar, view=self)


    @discord.ui.button(label=">|", custom_id='right_home', style=discord.ButtonStyle.blurple, row=0)
    async def right_home(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = self.max 
        embedVar = discord.Embed(color=0x89CFF0)

        self.right_button.disabled = True
        self.right_home.disabled = True
        self.left_button.disabled = False
        self.left_home.disabled = False

        self.page_number.label = f"{self.current_page + 1}/{self.max + 1}"


        x = self.embed_pages[self.max] 
        
        for i in range(0, len(x), 2):
            embedVar.add_field(name=x[i], value=x[i + 1], inline=False)

        await interaction.response.edit_message(embed=embedVar, view=self)
        
class ConfigButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)


    @discord.ui.button(label="Reset Infractions",style=discord.ButtonStyle.red)
    async def reset_infractions(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild = interaction.guild
        infraction_counts = {}
        for member in guild.members:
            infraction_counts[member.id] = 0
        with open(r'C:\Users\Mati\OneDrive\Desktop\Discord Slash Commands\moderation\moderation.json', 'w') as f:
            json.dump(infraction_counts, f)

        await interaction.response.edit_message(content='`resources\infractions.json reset`')




    @discord.ui.button(label="Reset Economy", style=discord.ButtonStyle.red)
    async def reset_economy(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild = interaction.guild
        default_total_balance = 1000
        default_bank_balance = 1000
        default_wallet_balance = 0
        default_job = None

        for member in guild.members:

            user_data = {}
            user_data['total_balance'] = default_total_balance
            user_data['bank_balance'] = default_bank_balance
            user_data['wallet_balance'] = default_wallet_balance
            user_data['job'] = default_job

            with open(r'C:\Users\Mati\OneDrive\Desktop\Discord Slash Commands\economy\economy.json', 'r') as f:
                data = json.load(f)

            users = data['users']
            users[str(member.id)] = user_data

            with open(r'C:\Users\Mati\OneDrive\Desktop\Discord Slash Commands\economy\economy.json', 'w') as f:
                json.dump({'users': users}, f)

        await interaction.response.edit_message(content='`economy\economy.json reset`')


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print(f'Class {self.__class__.__name__} loaded.')
    @app_commands.command(name="help", description="View the command list, and navigate though using pageination.")
    async def help(self, interaction: discord.Interaction):
        embedVar = discord.Embed(color=0x89CFF0, title='How to use Pageinator', description="""When you first see the page, it displays the first page of information. You can navigate to the next page by clicking on the `>` button or to the previous page by clicking on the `<` button. The `>|` button will take you to the last page, and the `|<` button will take you back to the first page.\n\nThe number in the middle of the buttons indicates the current page number, and it is not clickable. If you try to go beyond the first or last page, the corresponding buttons will become disabled, and you won't be able to click on them.""")
        await interaction.response.send_message(embed=embedVar, view=PageinatorButtons(), ephemeral=True)

class Config(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print(f'Class {self.__class__.__name__} loaded.')
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.command(name="config", description="administator permissions required")
    async def config(self, interaction: discord.Interaction):

        embedVar = discord.Embed()
        await interaction.response.send_message('`press buttons below to edit config files`', view=ConfigButtons(), ephemeral=True)
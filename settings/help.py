import discord
from discord import app_commands
from discord.ext import commands

class ConfirmationButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=45)

        self.embed_pages = 0

        self.embed_values = [

            ["/tictactoe", "Initiates a new game of Tic Tac Toe between the player and the computer."],
            ["Page 2 Title", "Page 2 Value"],
            ["Page 3 Title", "Page 3 Value"],
            ["Page 4 Title", "Page 4 Value"],
            ["Page 5 Title", "Page 5 Value"],
            ["Page 6 Title", "Page 6 Value"],
            ["Page 7 Title", "Page 7 Value"],
        ]


        self.max = len(self.embed_values) + 1
        self.min = 0


        self.embed_first_name = f'Page {self.min} Title'
        self.embed_first_value = f'Page {self.min} Value'


        self.embed_last_name = f'Page {self.max} Title'
        self.embed_last_value = f'Page {self.max} Value'
            
        
    @discord.ui.button(label="|<", custom_id='left_home', style=discord.ButtonStyle.blurple, row=0)
    async def left_home(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.embed_pages != self.min:
            self.embed_pages == self.min
        
        self.left_button.disabled = True
        self.left_home.disabled = True
        self.right_button.disabled = False
        self.right_home.disabled = False
        embedVar = discord.Embed(color=0x009a00)
        embedVar.add_field(name=self.embed_first_name, value=self.embed_first_value)
        await interaction.response.edit_message(embed=embedVar, view=self)

    @discord.ui.button(label="<", custom_id='left_button', style=discord.ButtonStyle.grey, row=0)
    async def left_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.embed_pages != self.min:
            self.embed_pages -= 1

        if self.embed_pages == self.min:
            self.left_button.disabled = True
            self.left_home.disabled = True
            self.right_button.disabled = False
            self.right_home.disabled = False
            embedVar = discord.Embed(color=0x009a00)
            embedVar.add_field(name=self.embed_first_name, value=self.embed_first_value)

        elif self.embed_pages == self.max:
            self.left_button.disabled = False
            self.left_home.disabled = False
            self.right_button.disabled = True
            self.right_home.disabled = True
            embedVar = discord.Embed(color=0x009a00)
            embedVar.add_field(name=self.embed_last_name, value=self.embed_last_value)

        elif self.embed_pages != self.min or self.embed_pages !=self.max:
            self.left_button.disabled = False
            self.right_button.disabled = False
            self.left_home.disabled = False
            self.right_home.disabled = False
            embedVar = discord.Embed(color=0x009a00)

            x = self.embed_values[self.embed_pages - 1] 
            embedVar.add_field(name=x[0], value=x[1])

        await interaction.response.edit_message(embed=embedVar, view=self)



    @discord.ui.button(label=">", custom_id='right_button', style=discord.ButtonStyle.grey, row=0)
    async def right_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.embed_pages != self.max:
            self.embed_pages += 1
        


        if self.embed_pages == self.min:
            self.left_button.disabled = True
            self.right_button.disabled = False
            embedVar = discord.Embed(color=0x009a00)
            embedVar.add_field(name=self.embed_first_name, value=self.embed_first_value)

        elif self.embed_pages == self.max:
            self.left_button.disabled = False
            self.left_home.disabled = False
            self.right_button.disabled = True
            self.right_home.disabled = True
            embedVar = discord.Embed(color=0x009a00)

            embedVar.add_field(name=self.embed_last_name, value=self.embed_last_value)
            print(self.embed_last_name, self.embed_last_value)


        elif self.embed_pages != self.min or self.embed_pages != self.max:
            self.left_button.disabled = False
            self.right_button.disabled = False
            self.left_home.disabled = False
            self.right_home.disabled = False
            embedVar = discord.Embed(color=0x009a00)


            x = self.embed_values[self.embed_pages - 1] 
            embedVar.add_field(name=x[0], value=x[1])

        await interaction.response.edit_message(embed=embedVar, view=self)


    @discord.ui.button(label=">|", custom_id='right_home', style=discord.ButtonStyle.blurple, row=0)
    async def right_home(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.embed_pages != self.max:
            self.embed_pages == self.max
        
        self.left_button.disabled = False
        self.left_home.disabled = False
        self.right_button.disabled = True
        self.right_home.disabled = True

        embedVar = discord.Embed(color=0x009a00)
        embedVar.add_field(name=self.embed_last_name, value=self.embed_last_value)
        await interaction.response.edit_message(embed=embedVar)
        

        



















class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @app_commands.command(name="help", description="view a command list")
    async def help(self, interaction: discord.Interaction):
        await interaction.response.send_message('Hi!', view=ConfirmationButtons(), ephemeral=True)



import json
import time
import random
import discord
from discord import app_commands
from discord.ext import commands


class Economy(commands.GroupCog, group_name='eco'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.emoji = [":gem:", ":first_place:", ":100:", ":dollar:", ":moneybag:", ":bell:"]

    def get_balance(self, user):
        with open('economy\economy.json', 'r') as f:
            data = json.load(f)

        print("Data Loaded")
        data['users'][str(user.id)]['total_balance'] 

        bank_balance = data['users'][str(user.id)]['bank_balance']
        wallet_balance = data['users'][str(user.id)]['wallet_balance']
        total_balance = data['users'][str(user.id)]['total_balance'] = wallet_balance + bank_balance
        return bank_balance, total_balance, wallet_balance

    def configure_balance(self, user, amount):
        with open('economy\economy.json', 'r') as f:
            data = json.load(f)

        data['users'][str(user.id)]['wallet_balance'] += amount
        bank_balance = data['users'][str(user.id)]['bank_balance']
        wallet_balance = data['users'][str(user.id)]['wallet_balance']
        total_balance = data['users'][str(user.id)]['total_balance'] = wallet_balance + bank_balance

        with open('economy\economy.json', 'w') as f:
            json.dump(data, f)

        return bank_balance, total_balance, wallet_balance

    def configure_bank(self, user):
        with open('economy\economy.json', 'r') as f:
            data = json.load(f)


        data['users'][str(user.id)]['bank_balance'] += data['users'][str(user.id)]['wallet_balance']
        data['users'][str(user.id)]['wallet_balance'] = 0


        bank_balance = data['users'][str(user.id)]['bank_balance']
        wallet_balance = data['users'][str(user.id)]['wallet_balance']
        total_balance = bank_balance + wallet_balance
        with open('economy\economy.json', 'w') as f:
            json.dump(data, f)

        return bank_balance, total_balance, wallet_balance


    @app_commands.command(name="balance", description="View your balance.")
    async def balance(self, interaction: discord.Interaction, user:discord.User=None):
        if user is None:
            user = interaction.user
            
        bank_balance, total_balance, wallet_balance = Economy.get_balance(self, user)
        embedVar = discord.Embed(color=0xEAAA00, title=f"{user.display_name}#{user.discriminator}'s Balance:",description=f"""Wallet Balance: 💸`{wallet_balance}`\n Bank Balance: 💸`{bank_balance}`\n Total Balance:   💸`{total_balance}` """)
        embedVar.set_footer(text=f'{interaction.user.display_name}#{interaction.user.discriminator}', icon_url=interaction.user.display_avatar.url)
        return await interaction.response.send_message(embed=embedVar, ephemeral=True)
   
    @app_commands.command(name="bank", description="Transfer coins from your wallet to the bank.")
    async def bank(self, interaction: discord.Interaction):
        user = interaction.user

        bank_balance, total_balance, wallet_balance = Economy.configure_bank(self, user)
        embedVar = discord.Embed(color=0xEAAA00, title=f"{user.display_name}#{user.discriminator}'s Updated Balance:",description=f"""Wallet Balance: 💸`{wallet_balance}`\n Bank Balance: 💸`{bank_balance}`\n Total Balance:   💸`{total_balance}` """)
        embedVar.set_footer(text=f'{interaction.user.display_name}#{interaction.user.discriminator}', icon_url=interaction.user.display_avatar.url)
        return await interaction.response.send_message(embed=embedVar, ephemeral=True)
        
    @app_commands.command(name="slots", description="Gamble your coins off with slot commands.")
    async def slots(self, interaction: discord.Interaction):
        one, two, three = random.choice(self.emoji), random.choice(self.emoji), random.choice(self.emoji)

        embedVar = discord.Embed(color=0xEAAA00)
        embedVar.add_field(name="Slot Machine!", value=f"<a:slot:1084337026586914857>|<a:slot:1084337026586914857>|<a:slot:1084337026586914857>")
        await interaction.response.send_message(embed=embedVar, ephemeral=True)
        time.sleep(1.5)

        embedVar = discord.Embed(color=0xEAAA00)
        embedVar.add_field(name="Slot Machine!", value=f"{one}|<a:slot:1084337026586914857>|<a:slot:1084337026586914857>")
        await interaction.edit_original_response(embed=embedVar)
        time.sleep(1.5)

        embedVar = discord.Embed(color=0xEAAA00)
        embedVar.add_field(name="Slot Machine!", value=f"{one}|{two}|<a:slot:1084337026586914857>")
        await interaction.edit_original_response(embed=embedVar)
        time.sleep(1.5)


        embedVar = discord.Embed(color=0xEAAA00)
        if one == two == three:
            profit = random.randint(100, 250)
            Economy.configure_balance(self, interaction.user, profit)
            embedVar.add_field(name="Jackpot!", value=f"{one}|{two}|{three}")
            embedVar.add_field(name="New Balance:", value=f"💸`{Economy.get_balance(self, interaction.user)[1]} (+{profit})`", inline=False)
            return await interaction.edit_original_response(embed=embedVar)

        elif one == two or one == three or two == three:
            profit = random.randint(20, 37)
            Economy.configure_balance(self, interaction.user, profit)
            embedVar.add_field(name="Close!", value=f"{one}|{two}|{three}")
            embedVar.add_field(name="New Balance:", value=f"💸`{Economy.get_balance(self, interaction.user)[1]} (+{profit})`", inline=False)
            return await interaction.edit_original_response(embed=embedVar)

        else:
            profit = random.randint(-10, 5)
            sign = '+' if profit > 0 else ''
            Economy.configure_balance(self, interaction.user, profit)
            embedVar.add_field(name="Nice Try!", value=f"{one}|{two}|{three}")
            embedVar.add_field(name="New Balance:", value=f"💸`{Economy.get_balance(self, interaction.user)[1]} ({sign}{profit})`", inline=False)
            return await interaction.edit_original_response(embed=embedVar)

    @app_commands.command(name="rob", description="rob someone")
    async def rob(self, interaction: discord.Interaction, user:discord.User):
        wallet_balance = Economy.get_balance(self, user)[2] 
        amount = wallet_balance / random.randint(2, 4)

        print(wallet_balance)

        if wallet_balance > 0 and random.randint(1, 2) == 1: # if user has wallet balance > 0, rob successful



            Economy.configure_balance(self, interaction.user, amount)
            Economy.configure_balance(self, user, -amount)
            embedVar = discord.Embed(color=0xEAAA00)
            embedVar.add_field(name=f"{user.display_name}#{user.discriminator} Has Been Robbed!", value=f"New Wallet Balance: 💸`{Economy.get_balance(self, interaction.user)[1]} (+{amount})`")
            embedVar.set_footer(text=f'{interaction.user.display_name}#{interaction.user.discriminator}', icon_url=interaction.user.display_avatar.url)
            return await interaction.response.send_message(embed=embedVar, ephemeral=True)


        else: #  bad
            amount = random.randint(100, 250)

            Economy.configure_balance(self, interaction.user, -amount)
            embedVar = discord.Embed(color=0xCE2029)
            embedVar.add_field(name=f"🚔🚨 You've Been Caught!", value=f"New Wallet Balance: 💸`{Economy.get_balance(self, interaction.user)[1]} (-{amount})`")
            embedVar.set_footer(text=f'{interaction.user.display_name}#{interaction.user.discriminator}', icon_url=interaction.user.display_avatar.url)
            return await interaction.response.send_message(embed=embedVar, ephemeral=True)  


      

            








    #rob command only works for users that have not banked money
    #can still rob users with banked money, but chances decrease significantly
    #owned bank determines the safety of your money
    #can purchase safer banks and autobanking(the earnt money auto transfers to the bank)
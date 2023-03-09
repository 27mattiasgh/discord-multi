import json
import random
import discord
from cogs.engine import Engine
from discord import app_commands
from discord.ext import commands

class TicTacToeButtons(discord.ui.View):
    def __init__(self, own_piece, computer_piece, board):
        super().__init__(timeout=45)

        self.own_piece = own_piece
        self.computer_piece = computer_piece
        if self.own_piece == 1:
            own_piece_char = 'X'
            self.own_piece_char = own_piece_char
            computer_piece_char = 'O'
            self.computer_piece_char = computer_piece_char
        else:
            own_piece_char = 'O'
            self.own_piece_char = own_piece_char       
            computer_piece_char = 'X'
            self.computer_piece_char = computer_piece_char


        self.board = board

    @discord.ui.button(label="ㅤ", custom_id='square_zero', style=discord.ButtonStyle.grey, row=0)
    async def square_zero(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.board.count(0) == 9:

            if self.own_piece == 1: #if own piece is X
                self.square_zero.style = discord.ButtonStyle.green
                self.square_zero.label = self.own_piece_char
                self.board[0] = self.own_piece
                custom_board = [x * -1 for x in self.board]
                result = Engine(custom_board)

            if self.own_piece == -1: 
                result = 0

             
        else:
            self.square_zero.style = discord.ButtonStyle.green
            self.square_zero.label = self.own_piece_char
            if self.own_piece == 1: #if own piece is X
                self.board[0] = self.own_piece
                custom_board = [x * -1 for x in self.board]
                result = Engine(custom_board)
            else:
                self.board[0] = self.own_piece
                result = Engine(self.board)

        self.board[result] = self.computer_piece
        print(result, self.board, 'squ0')

        if result == 0:
            self.square_zero.style = discord.ButtonStyle.red
            self.square_zero.label = self.computer_piece_char
        elif result == 1:
            self.square_one.style = discord.ButtonStyle.red      
            self.square_one.label = self.computer_piece_char
        elif result == 2:
            self.square_two.style = discord.ButtonStyle.red
            self.square_two.label = self.computer_piece_char
        elif result == 3:
            self.square_three.style = discord.ButtonStyle.red        
            self.square_three.label = self.computer_piece_char
        elif result == 4:
            self.square_four.style = discord.ButtonStyle.red
            self.square_four.label = self.computer_piece_char
        elif result == 5:
            self.square_five.style = discord.ButtonStyle.red
            self.square_five.label = self.computer_piece_char
        elif result == 6:
            self.square_six.style = discord.ButtonStyle.red
            self.square_six.label = self.computer_piece_char                  
        elif result == 7:
            self.square_seven.style = discord.ButtonStyle.red
            self.square_seven.label = self.computer_piece_char     
        elif result == 8:
            self.square_eight.style = discord.ButtonStyle.red
            self.square_eight.label = self.computer_piece_char 

        if self.board.count(0) == 0:
            self.square_zero.disabled = True
            self.square_one.disabled = True
            self.square_two.disabled = True
            self.square_three.disabled = True
            self.square_four.disabled = True
            self.square_five.disabled = True
            self.square_six.disabled = True
            self.square_seven.disabled = True
            self.square_eight.disabled = True 
            return await interaction.response.edit_message(content='Game Over!', view=self)
        await interaction.response.edit_message(content='Your Move!', view=self)

    



    @discord.ui.button(label="ㅤ", custom_id='square_one', style=discord.ButtonStyle.grey, row=0)
    async def square_one(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.board.count(0) == 9:
            if self.own_piece == 1: #if own piece is X
                self.square_one.style = discord.ButtonStyle.green
                self.square_one.label = self.own_piece_char
                self.board[1] = self.own_piece
                self.board = [x * -1 for x in self.board]
                result = Engine(custom_board)
            if self.own_piece == -1: 
                result = 0
        else:
            self.square_one.style = discord.ButtonStyle.green
            self.square_one.label = self.own_piece_char
            if self.own_piece == 1: #if own piece is X
                self.board[1] = self.own_piece
                custom_board = [x * -1 for x in self.board]
                result = Engine(custom_board)
            else:
                self.board[1] = self.own_piece
                result = Engine(self.board)

        self.board[result] = self.computer_piece
        print(result, self.board, 'squ1')

        if result == 0:
            self.square_zero.style = discord.ButtonStyle.red
            self.square_zero.label = self.computer_piece_char
        elif result == 1:
                self.square_one.style = discord.ButtonStyle.red      
                self.square_one.label = self.computer_piece_char
        elif result == 2:
            self.square_two.style = discord.ButtonStyle.red
            self.square_two.label = self.computer_piece_char
        elif result == 3:
            self.square_three.style = discord.ButtonStyle.red        
            self.square_three.label = self.computer_piece_char
        elif result == 4:
            self.square_four.style = discord.ButtonStyle.red
            self.square_four.label = self.computer_piece_char
        elif result == 5:
            self.square_five.style = discord.ButtonStyle.red
            self.square_five.label = self.computer_piece_char
        elif result == 6:
            self.square_six.style = discord.ButtonStyle.red
            self.square_six.label = self.computer_piece_char                  
        elif result == 7:
            self.square_seven.style = discord.ButtonStyle.red
            self.square_seven.label = self.computer_piece_char     
        elif result == 8:
            self.square_eight.style = discord.ButtonStyle.red
            self.square_eight.label = self.computer_piece_char 

        if self.board.count(0) == 0:
            self.square_zero.disabled = True
            self.square_one.disabled = True
            self.square_two.disabled = True
            self.square_three.disabled = True
            self.square_four.disabled = True
            self.square_five.disabled = True
            self.square_six.disabled = True
            self.square_seven.disabled = True
            self.square_eight.disabled = True 
            return await interaction.response.edit_message(content='Game Over!', view=self)
        await interaction.response.edit_message(content='Your Move!', view=self)

    @discord.ui.button(label="ㅤ", custom_id='square_two', style=discord.ButtonStyle.grey, row=0)
    async def square_two(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.board.count(0) == 9:
            if self.own_piece == 1: #if own piece is X
                self.square_two.style = discord.ButtonStyle.green
                self.square_two.label = self.own_piece_char
                self.board[2] = self.own_piece
                custom_board = [x * -1 for x in self.board]
                result = Engine(custom_board)
            if self.own_piece == -1: 
                result = 0
        else:
            self.square_two.style = discord.ButtonStyle.green
            self.square_two.label = self.own_piece_char
            if self.own_piece == 1: #if own piece is X
                self.board[2] = self.own_piece
                custom_board = [x * -1 for x in self.board]
                result = Engine(custom_board)
            else:
                self.board[2] = self.own_piece
                result = Engine(self.board)

        self.board[result] = self.computer_piece
        print(result, self.board, 'squ2')

        if result == 0:
            self.square_zero.style = discord.ButtonStyle.red
            self.square_zero.label = self.computer_piece_char
        elif result == 1:
            self.square_one.style = discord.ButtonStyle.red      
            self.square_one.label = self.computer_piece_char
        elif result == 2:
            self.square_two.style = discord.ButtonStyle.red
            self.square_two.label = self.computer_piece_char
        elif result == 3:
            self.square_three.style = discord.ButtonStyle.red        
            self.square_three.label = self.computer_piece_char
        elif result == 4:
            self.square_four.style = discord.ButtonStyle.red
            self.square_four.label = self.computer_piece_char
        elif result == 5:
            self.square_five.style = discord.ButtonStyle.red
            self.square_five.label = self.computer_piece_char
        elif result == 6:
            self.square_six.style = discord.ButtonStyle.red
            self.square_six.label = self.computer_piece_char                  
        elif result == 7:
            self.square_seven.style = discord.ButtonStyle.red
            self.square_seven.label = self.computer_piece_char     
        elif result == 8:
            self.square_eight.style = discord.ButtonStyle.red
            self.square_eight.label = self.computer_piece_char 

        if self.board.count(0) == 0:
            self.square_zero.disabled = True
            self.square_one.disabled = True
            self.square_two.disabled = True
            self.square_three.disabled = True
            self.square_four.disabled = True
            self.square_five.disabled = True
            self.square_six.disabled = True
            self.square_seven.disabled = True
            self.square_eight.disabled = True 
            return await interaction.response.edit_message(content='Game Over!', view=self)
        await interaction.response.edit_message(content='Your Move!', view=self)


    @discord.ui.button(label="ㅤ", custom_id='square_three', style=discord.ButtonStyle.grey, row=1)
    async def square_three(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.board.count(0) == 9:
            if self.own_piece == 1: #if own piece is X
                self.square_three.style = discord.ButtonStyle.green
                self.square_three.label = self.own_piece_char
                self.board[3] = self.own_piece
                custom_board = [x * -1 for x in self.board]
                result = Engine(custom_board)
            if self.own_piece == -1: 
                result = 0
        else:

            self.square_three.style = discord.ButtonStyle.green
            self.square_three.label = self.own_piece_char

            if self.own_piece == 1: #if own piece is X
                self.board[3] = self.own_piece
                custom_board = [x * -1 for x in self.board]
                result = Engine(custom_board)
            else:
                self.board[3] = self.own_piece
                result = Engine(self.board)

        self.board[result] = self.computer_piece
        print(result, self.board, 'squ3')

        if result == 0:
            self.square_zero.style = discord.ButtonStyle.red
            self.square_zero.label = self.computer_piece_char
        elif result == 1:
            self.square_one.style = discord.ButtonStyle.red      
            self.square_one.label = self.computer_piece_char
        elif result == 2:
            self.square_two.style = discord.ButtonStyle.red
            self.square_two.label = self.computer_piece_char
        elif result == 3:
            self.square_three.style = discord.ButtonStyle.red        
            self.square_three.label = self.computer_piece_char
        elif result == 4:
            self.square_four.style = discord.ButtonStyle.red
            self.square_four.label = self.computer_piece_char
        elif result == 5:
            self.square_five.style = discord.ButtonStyle.red
            self.square_five.label = self.computer_piece_char
        elif result == 6:
            self.square_six.style = discord.ButtonStyle.red
            self.square_six.label = self.computer_piece_char                  
        elif result == 7:
            self.square_seven.style = discord.ButtonStyle.red
            self.square_seven.label = self.computer_piece_char     
        elif result == 8:
            self.square_eight.style = discord.ButtonStyle.red
            self.square_eight.label = self.computer_piece_char 

        if self.board.count(0) == 0:
            self.square_zero.disabled = True
            self.square_one.disabled = True
            self.square_two.disabled = True
            self.square_three.disabled = True
            self.square_four.disabled = True
            self.square_five.disabled = True
            self.square_six.disabled = True
            self.square_seven.disabled = True
            self.square_eight.disabled = True 
            return await interaction.response.edit_message(content='Game Over!', view=self)
        await interaction.response.edit_message(content='Your Move!', view=self)

    @discord.ui.button(label="ㅤ", custom_id='square_four', style=discord.ButtonStyle.grey, row=1)
    async def square_four(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.board.count(0) == 9:
            if self.own_piece == 1: #if own piece is X
                self.square_four.style = discord.ButtonStyle.green
                self.square_four.label = self.own_piece_char
                self.board[4] = self.own_piece
                custom_board = [x * -1 for x in self.board]
                result = Engine(custom_board)
            if self.own_piece == -1: 
                result = 0
        else:
            self.square_four.style = discord.ButtonStyle.green
            self.square_four.label = self.own_piece_char
            if self.own_piece == 1: #if own piece is X
                self.board[4] = self.own_piece
                custom_board = [x * -1 for x in self.board]
                result = Engine(custom_board)
            else:
                self.board[4] = self.own_piece
                result = Engine(self.board)

        self.board[result] = self.computer_piece
        print(result, self.board, 'squ4')

        if result == 0:
                self.square_zero.style = discord.ButtonStyle.red
                self.square_zero.label = self.computer_piece_char
        elif result == 1:
                self.square_one.style = discord.ButtonStyle.red      
                self.square_one.label = self.computer_piece_char
        elif result == 2:
                self.square_two.style = discord.ButtonStyle.red
                self.square_two.label = self.computer_piece_char
        elif result == 3:
                self.square_three.style = discord.ButtonStyle.red        
                self.square_three.label = self.computer_piece_char
        elif result == 4:
                self.square_four.style = discord.ButtonStyle.red
                self.square_four.label = self.computer_piece_char
        elif result == 5:
                self.square_five.style = discord.ButtonStyle.red
                self.square_five.label = self.computer_piece_char
        elif result == 6:
                self.square_six.style = discord.ButtonStyle.red
                self.square_six.label = self.computer_piece_char                  
        elif result == 7:
                self.square_seven.style = discord.ButtonStyle.red
                self.square_seven.label = self.computer_piece_char     
        elif result == 8:
                self.square_eight.style = discord.ButtonStyle.red
                self.square_eight.label = self.computer_piece_char 

        if self.board.count(0) == 0:
            self.square_zero.disabled = True
            self.square_one.disabled = True
            self.square_two.disabled = True
            self.square_three.disabled = True
            self.square_four.disabled = True
            self.square_five.disabled = True
            self.square_six.disabled = True
            self.square_seven.disabled = True
            self.square_eight.disabled = True 
            return await interaction.response.edit_message(content='Game Over!', view=self)
        await interaction.response.edit_message(content='Your Move!', view=self)

    @discord.ui.button(label="ㅤ", custom_id='square_five', style=discord.ButtonStyle.grey, row=1)
    async def square_five(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.board.count(0) == 9:
            if self.own_piece == 1: #if own piece is X
                self.square_five.style = discord.ButtonStyle.green
                self.square_five.label = self.own_piece_char
                self.board[5] = self.own_piece
                custom_board = [x * -1 for x in self.board]
                result = Engine(custom_board)

            if self.own_piece == -1: 
                result = 0
        else:
            self.square_five.style = discord.ButtonStyle.green
            self.square_five.label = self.own_piece_char
            if self.own_piece == 1: #if own piece is X
                self.board[5] = self.own_piece
                custom_board = [x * -1 for x in self.board]
                result = Engine(custom_board)
            else:
                self.board[5] = self.own_piece
                result = Engine(self.board)

        self.board[result] = self.computer_piece
        print(result, self.board, 'squ5')

        if result == 0:
                self.square_zero.style = discord.ButtonStyle.red
                self.square_zero.label = self.computer_piece_char
        elif result == 1:
                self.square_one.style = discord.ButtonStyle.red      
                self.square_one.label = self.computer_piece_char
        elif result == 2:
                self.square_two.style = discord.ButtonStyle.red
                self.square_two.label = self.computer_piece_char
        elif result == 3:
                self.square_three.style = discord.ButtonStyle.red        
                self.square_three.label = self.computer_piece_char
        elif result == 4:
                self.square_four.style = discord.ButtonStyle.red
                self.square_four.label = self.computer_piece_char
        elif result == 5:
                self.square_five.style = discord.ButtonStyle.red
                self.square_five.label = self.computer_piece_char
        elif result == 6:
                self.square_six.style = discord.ButtonStyle.red
                self.square_six.label = self.computer_piece_char                  
        elif result == 7:
                self.square_seven.style = discord.ButtonStyle.red
                self.square_seven.label = self.computer_piece_char     
        elif result == 8:
                self.square_eight.style = discord.ButtonStyle.red
                self.square_eight.label = self.computer_piece_char 

        if self.board.count(0) == 0:
            self.square_zero.disabled = True
            self.square_one.disabled = True
            self.square_two.disabled = True
            self.square_three.disabled = True
            self.square_four.disabled = True
            self.square_five.disabled = True
            self.square_six.disabled = True
            self.square_seven.disabled = True
            self.square_eight.disabled = True 
            return await interaction.response.edit_message(content='Game Over!', view=self)
        await interaction.response.edit_message(content='Your Move!', view=self)

    @discord.ui.button(label="ㅤ", custom_id='square_six', style=discord.ButtonStyle.grey, row=2)
    async def square_six(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.board.count(0) == 9:
            if self.own_piece == 1: #if own piece is X
                self.square_six.style = discord.ButtonStyle.green
                self.square_six.label = self.own_piece_char
                self.board[6] = self.own_piece
                custom_board = [x * -1 for x in self.board]
                result = Engine(custom_board)
            if self.own_piece == -1: 
                result = 0
        else:
            self.square_six.style = discord.ButtonStyle.green
            self.square_six.label = self.own_piece_char
            if self.own_piece == 1: #if own piece is X
                self.board[6] = self.own_piece
                custom_board = [x * -1 for x in self.board]
                result = Engine(custom_board)
            else:
                self.board[6] = self.own_piece
                result = Engine(self.board)

        self.board[result] = self.computer_piece
        print(result, self.board, 'squ6')

        if result == 0:
                self.square_zero.style = discord.ButtonStyle.red
                self.square_zero.label = self.computer_piece_char
        elif result == 1:
                self.square_one.style = discord.ButtonStyle.red      
                self.square_one.label = self.computer_piece_char
        elif result == 2:
                self.square_two.style = discord.ButtonStyle.red
                self.square_two.label = self.computer_piece_char
        elif result == 3:
                self.square_three.style = discord.ButtonStyle.red        
                self.square_three.label = self.computer_piece_char
        elif result == 4:
                self.square_four.style = discord.ButtonStyle.red
                self.square_four.label = self.computer_piece_char
        elif result == 5:
                self.square_five.style = discord.ButtonStyle.red
                self.square_five.label = self.computer_piece_char
        elif result == 6:
                self.square_six.style = discord.ButtonStyle.red
                self.square_six.label = self.computer_piece_char                  
        elif result == 7:
                self.square_seven.style = discord.ButtonStyle.red
                self.square_seven.label = self.computer_piece_char     
        elif result == 8:
                self.square_eight.style = discord.ButtonStyle.red
                self.square_eight.label = self.computer_piece_char 

        if self.board.count(0) == 0:
            self.square_zero.disabled = True
            self.square_one.disabled = True
            self.square_two.disabled = True
            self.square_three.disabled = True
            self.square_four.disabled = True
            self.square_five.disabled = True
            self.square_six.disabled = True
            self.square_seven.disabled = True
            self.square_eight.disabled = True 
            return await interaction.response.edit_message(content='Game Over!', view=self)
        await interaction.response.edit_message(content='Your Move!', view=self)

    @discord.ui.button(label="ㅤ", custom_id='square_seven', style=discord.ButtonStyle.grey, row=2)
    async def square_seven(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.board.count(0) == 9:
            if self.own_piece == 1: #if own piece is X
                self.square_seven.style = discord.ButtonStyle.green
                self.square_seven.label = self.own_piece_char
                self.board[7] = self.own_piece
                custom_board = [x * -1 for x in self.board]
                result = Engine(custom_board)
            if self.own_piece == -1: 
                result = 0
        else:
            self.square_seven.style = discord.ButtonStyle.green
            self.square_seven.label = self.own_piece_char
            if self.own_piece == 1: #if own piece is X
                self.board[7] = self.own_piece
                custom_board = [x * -1 for x in self.board]
                result = Engine(custom_board)
            else:
                self.board[7] = self.own_piece
                result = Engine(self.board)
    
        self.board[result] = self.computer_piece
        print(result, self.board, 'squ7')

        if result == 0:
            self.square_zero.style = discord.ButtonStyle.red
            self.square_zero.label = self.computer_piece_char
        elif result == 1:
            self.square_one.style = discord.ButtonStyle.red      
            self.square_one.label = self.computer_piece_char
        elif result == 2:
            self.square_two.style = discord.ButtonStyle.red
            self.square_two.label = self.computer_piece_char
        elif result == 3:
            self.square_three.style = discord.ButtonStyle.red        
            self.square_three.label = self.computer_piece_char
        elif result == 4:
            self.square_four.style = discord.ButtonStyle.red
            self.square_four.label = self.computer_piece_char
        elif result == 5:
            self.square_five.style = discord.ButtonStyle.red
            self.square_five.label = self.computer_piece_char
        elif result == 6:
            self.square_six.style = discord.ButtonStyle.red
            self.square_six.label = self.computer_piece_char                  
        elif result == 7:
            self.square_seven.style = discord.ButtonStyle.red
            self.square_seven.label = self.computer_piece_char     
        elif result == 8:
            self.square_eight.style = discord.ButtonStyle.red
            self.square_eight.label = self.computer_piece_char 

        if self.board.count(0) == 0:
            self.square_zero.disabled = True
            self.square_one.disabled = True
            self.square_two.disabled = True
            self.square_three.disabled = True
            self.square_four.disabled = True
            self.square_five.disabled = True
            self.square_six.disabled = True
            self.square_seven.disabled = True
            self.square_eight.disabled = True 
            return await interaction.response.edit_message(content='Game Over!', view=self)
        await interaction.response.edit_message(content='Your Move!', view=self)
    
    @discord.ui.button(label="ㅤ", custom_id='square_eight', style=discord.ButtonStyle.grey, row=2)
    async def square_eight(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.board.count(0) == 9:
            if self.own_piece == 1: #if own piece is X
                self.square_eight.style = discord.ButtonStyle.green
                self.square_eight.label = self.own_piece_char
                self.board[8] = self.own_piece
                custom_board = [x * -1 for x in self.board]
                result = Engine(custom_board)

            if self.own_piece == -1: 
                result = 0
        else:
            self.square_eight.style = discord.ButtonStyle.green
            self.square_eight.label = self.own_piece_char
            if self.own_piece == 1: #if own piece is X
                self.board[8] = self.own_piece
                custom_board = [x * -1 for x in self.board]
                result = Engine(custom_board)
            else:
                self.board[8] = self.own_piece
                result = Engine(self.board)

        self.board[result] = self.computer_piece
        print(result, self.board, 'squ8')

        if result == 0:
                self.square_zero.style = discord.ButtonStyle.red
                self.square_zero.label = self.computer_piece_char
        elif result == 1:
                self.square_one.style = discord.ButtonStyle.red      
                self.square_one.label = self.computer_piece_char
        elif result == 2:
                self.square_two.style = discord.ButtonStyle.red
                self.square_two.label = self.computer_piece_char
        elif result == 3:
                self.square_three.style = discord.ButtonStyle.red        
                self.square_three.label = self.computer_piece_char
        elif result == 4:
                self.square_four.style = discord.ButtonStyle.red
                self.square_four.label = self.computer_piece_char
        elif result == 5:
                self.square_five.style = discord.ButtonStyle.red
                self.square_five.label = self.computer_piece_char
        elif result == 6:
                self.square_six.style = discord.ButtonStyle.red
                self.square_six.label = self.computer_piece_char                  
        elif result == 7:
                self.square_seven.style = discord.ButtonStyle.red
                self.square_seven.label = self.computer_piece_char     
        elif result == 8:
                self.square_eight.style = discord.ButtonStyle.red
                self.square_eight.label = self.computer_piece_char 

        if self.board.count(0) == 0:
            self.square_zero.disabled = True
            self.square_one.disabled = True
            self.square_two.disabled = True
            self.square_three.disabled = True
            self.square_four.disabled = True
            self.square_five.disabled = True
            self.square_six.disabled = True
            self.square_seven.disabled = True
            self.square_eight.disabled = True 
            return await interaction.response.edit_message(content='Game Over!', view=self)
        await interaction.response.edit_message(content='Your Move!', view=self)


 
 
class TestSelection(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=45)
    @discord.ui.select(placeholder = "Choose a Flavor!", min_values = 1, max_values = 2,
        options = [
         
            discord.SelectOption(label="Vanilla", description="Pick this if you like vanilla!"),

        ]
    )

    async def select_callback(self, interaction:discord.Interaction, select):
        if select.values[0] == "Chocolate":
            return await interaction.response.send_message(f"F you. No one likes {select.values[0]}!")
        if len(select.values) > 1:
            return await interaction.response.send_message(f"Awesome! I like {select.values[0]} and {select.values[1]} too!")
        return await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")




class Tictactoe(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @app_commands.command(name="tictactoe", description="play tic-tac-toe against the computer")
    async def tictactoe(self, interaction: discord.Interaction):
        
        piece = random.randint(1,2)

        board = [0, 0, 0, 
                 0, 0, 0, 
                 0, 0, 0]

        if piece == 2:
            piece = -1
            return await interaction.response.send_message('The computer goes first - Click any button to start!', view=TicTacToeButtons(piece, -piece, board),ephemeral=True)
        
        return await interaction.response.send_message('Your Move!', view=TicTacToeButtons(piece, -piece, board),ephemeral=True)
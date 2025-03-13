import discord
from discord.ext import commands
import asyncio
import random

class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}
        
    def create_board(self):
        return [["\u200b" for _ in range(3)] for _ in range(3)]
        
    def make_embed(self, board, turn):
        embed = discord.Embed(
            title="Tic Tac Toe",
            description=f"Current turn: {turn}",
            color=self.bot.colors['primary']
        )
        board_str = ""
        for row in board:
            board_str += "".join([":o:" if cell == "O" else ":x:" if cell == "X" else "⬜" for cell in row]) + "\n"
        embed.add_field(name="Board", value=board_str)
        return embed
        
    def check_winner(self, board):
        # Check rows, columns and diagonals
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != "\u200b":
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != "\u200b":
                return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != "\u200b":
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != "\u200b":
            return board[0][2]
        return None
        
    @commands.command()
    async def tictactoe(self, ctx, opponent: discord.Member):
        """Play Tic Tac Toe with another user"""
        if opponent.bot or opponent == ctx.author:
            await ctx.send("You can't play against a bot or yourself!")
            return
            
        board = self.create_board()
        current_player = ctx.author
        players = {ctx.author: "X", opponent: "O"}
        
        message = await ctx.send(embed=self.make_embed(board, current_player.mention))
        
        for emoji in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]:
            await message.add_reaction(emoji)
            
        def check(reaction, user):
            return user == current_player and str(reaction.emoji) in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
            
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                position = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"].index(str(reaction.emoji))
                row = position // 3
                col = position % 3
                
                if board[row][col] == "\u200b":
                    board[row][col] = players[current_player]
                    winner = self.check_winner(board)
                    
                    if winner:
                        await message.edit(embed=discord.Embed(
                            title="Game Over!",
                            description=f"{current_player.mention} ({winner}) wins!",
                            color=self.bot.colors['success']
                        ))
                        break
                        
                    if all(cell != "\u200b" for row in board for cell in row):
                        await message.edit(embed=discord.Embed(
                            title="Game Over!",
                            description="It's a tie!",
                            color=self.bot.colors['secondary']
                        ))
                        break
                        
                    current_player = opponent if current_player == ctx.author else ctx.author
                    await message.edit(embed=self.make_embed(board, current_player.mention))
                
                await message.remove_reaction(reaction.emoji, user)
                
            except asyncio.TimeoutError:
                await message.edit(embed=discord.Embed(
                    title="Game Over!",
                    description="Game timed out due to inactivity",
                    color=self.bot.colors['error']
                ))
                break

async def setup(bot):
    await bot.add_cog(TicTacToe(bot))

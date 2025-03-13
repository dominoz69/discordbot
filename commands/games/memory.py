import discord
from discord.ext import commands
import random
import asyncio

class Memory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = ['🍎', '🍌', '🍇', '🍊', '🍓', '🍉', '🍍', '🥝', '🥑', '🥕']
        
    def create_board(self, size=4):
        """Create a memory game board"""
        if size % 2 != 0:
            size += 1
        pairs = (size * size) // 2
        cards = random.sample(self.emojis, pairs) * 2
        random.shuffle(cards)
        return [cards[i:i + size] for i in range(0, len(cards), size)]
        
    def format_board(self, board, revealed):
        """Format the board for display"""
        output = ""
        for i, row in enumerate(board):
            for j, card in enumerate(row):
                pos = i * len(board) + j
                if pos in revealed:
                    output += card + " "
                else:
                    output += "⬜ "
            output += "\n"
        return output
        
    @commands.command()
    async def memory(self, ctx, size: int = 4):
        """Play a memory card matching game"""
        if size < 2 or size > 6:
            await ctx.send("Size must be between 2 and 6!")
            return
            
        board = self.create_board(size)
        revealed = set()
        current_selection = []
        pairs_found = 0
        total_pairs = (size * size) // 2
        moves = 0
        
        embed = discord.Embed(
            title="Memory Game",
            description=f"Match pairs of cards! Select positions (1-{size*size})\n\n" + 
                       self.format_board(board, revealed),
            color=self.bot.colors['primary']
        )
        message = await ctx.send(embed=embed)
        
        def check(m):
            return (m.author == ctx.author and m.channel == ctx.channel and 
                   m.content.isdigit() and 1 <= int(m.content) <= size * size)
            
        while pairs_found < total_pairs:
            try:
                guess = await self.bot.wait_for('message', timeout=30.0, check=check)
                pos = int(guess.content) - 1
                
                if pos in revealed:
                    await ctx.send("That card is already revealed!", delete_after=2)
                    continue
                    
                row, col = pos // size, pos % size
                current_selection.append((pos, board[row][col]))
                revealed.add(pos)
                moves += 1
                
                embed = discord.Embed(
                    title="Memory Game",
                    description=self.format_board(board, revealed),
                    color=self.bot.colors['primary']
                )
                await message.edit(embed=embed)
                
                if len(current_selection) == 2:
                    if current_selection[0][1] == current_selection[1][1]:
                        pairs_found += 1
                        await ctx.send("Match found! 🎉", delete_after=2)
                    else:
                        await asyncio.sleep(1)
                        revealed.remove(current_selection[0][0])
                        revealed.remove(current_selection[1][0])
                        embed = discord.Embed(
                            title="Memory Game",
                            description=self.format_board(board, revealed),
                            color=self.bot.colors['primary']
                        )
                        await message.edit(embed=embed)
                    current_selection = []
                    
            except asyncio.TimeoutError:
                timeout_embed = discord.Embed(
                    title="Game Over",
                    description="Time's up! Game cancelled.",
                    color=self.bot.colors['error']
                )
                await message.edit(embed=timeout_embed)
                return
                
        win_embed = discord.Embed(
            title="Congratulations! 🎉",
            description=f"You found all pairs in {moves} moves!",
            color=self.bot.colors['success']
        )
        await message.edit(embed=win_embed)

async def setup(bot):
    await bot.add_cog(Memory(bot))

import discord
from discord.ext import commands
import random
import asyncio

class RockPaperScissors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = {
            "rock": "🪨",
            "paper": "📄",
            "scissors": "✂️"
        }
        
    @commands.command(aliases=['rps'])
    async def rockpaperscissors(self, ctx, opponent: discord.Member = None):
        """Play Rock Paper Scissors!"""
        if opponent and (opponent.bot or opponent == ctx.author):
            await ctx.send("You can't play against a bot or yourself!")
            return
            
        embed = discord.Embed(
            title="Rock Paper Scissors",
            description="Choose your move!",
            color=self.bot.colors['primary']
        )
        message = await ctx.send(embed=embed)
        
        for emoji in self.emojis.values():
            await message.add_reaction(emoji)
            
        if opponent:
            # PvP mode
            players = {ctx.author: None, opponent: None}
            
            def check(reaction, user):
                return user in players and str(reaction.emoji) in self.emojis.values()
                
            try:
                for _ in range(2):
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                    players[user] = str(reaction.emoji)
                    
                moves = {v: k for k, v in self.emojis.items()}
                p1_move = moves[players[ctx.author]]
                p2_move = moves[players[opponent]]
                
                winner = self.get_winner(p1_move, p2_move)
                
                if winner == "tie":
                    result = "It's a tie!"
                    color = self.bot.colors['secondary']
                else:
                    winner_player = ctx.author if winner == p1_move else opponent
                    result = f"{winner_player.mention} wins!"
                    color = self.bot.colors['success']
                    
                embed = discord.Embed(
                    title="Game Over!",
                    description=f"{ctx.author.mention}: {players[ctx.author]}\n{opponent.mention}: {players[opponent]}\n\n{result}",
                    color=color
                )
                await message.edit(embed=embed)
                
            except asyncio.TimeoutError:
                await message.edit(embed=discord.Embed(
                    title="Game Over!",
                    description="Game timed out due to inactivity",
                    color=self.bot.colors['error']
                ))
                
        else:
            # PvE mode
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in self.emojis.values()
                
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                moves = {v: k for k, v in self.emojis.items()}
                player_move = moves[str(reaction.emoji)]
                bot_move = random.choice(list(self.emojis.keys()))
                
                winner = self.get_winner(player_move, bot_move)
                
                if winner == "tie":
                    result = "It's a tie!"
                    color = self.bot.colors['secondary']
                else:
                    result = "You win!" if winner == player_move else "Bot wins!"
                    color = self.bot.colors['success'] if winner == player_move else self.bot.colors['error']
                    
                embed = discord.Embed(
                    title="Game Over!",
                    description=f"You: {self.emojis[player_move]}\nBot: {self.emojis[bot_move]}\n\n{result}",
                    color=color
                )
                await message.edit(embed=embed)
                
            except asyncio.TimeoutError:
                await message.edit(embed=discord.Embed(
                    title="Game Over!",
                    description="Game timed out due to inactivity",
                    color=self.bot.colors['error']
                ))
                
    def get_winner(self, move1, move2):
        if move1 == move2:
            return "tie"
        wins = {
            "rock": "scissors",
            "paper": "rock",
            "scissors": "paper"
        }
        return move1 if wins[move1] == move2 else move2

async def setup(bot):
    await bot.add_cog(RockPaperScissors(bot))

import discord
from discord.ext import commands
import random
import asyncio

class MathGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.operations = ['+', '-', '*']
        self.difficulties = {
            'easy': (1, 10),
            'medium': (10, 50),
            'hard': (50, 100)
        }
        
    def generate_problem(self, difficulty='medium'):
        num_range = self.difficulties.get(difficulty, self.difficulties['medium'])
        num1 = random.randint(*num_range)
        num2 = random.randint(*num_range)
        operation = random.choice(self.operations)
        
        if operation == '+':
            answer = num1 + num2
        elif operation == '-':
            answer = num1 - num2
        else:  # multiplication
            num2 = random.randint(2, 12)  # Keep multiplication reasonable
            answer = num1 * num2
            
        return f"{num1} {operation} {num2}", answer
        
    @commands.command()
    async def mathgame(self, ctx, difficulty: str = 'medium'):
        """Play a math game! Solve arithmetic problems quickly"""
        if difficulty not in self.difficulties:
            await ctx.send(f"Invalid difficulty! Choose from: {', '.join(self.difficulties.keys())}")
            return
            
        problem, answer = self.generate_problem(difficulty)
        
        embed = discord.Embed(
            title="Math Game",
            description=f"Solve this problem:\n{problem} = ?\nYou have 15 seconds!",
            color=self.bot.colors['primary']
        )
        await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lstrip('-').isdigit()
            
        try:
            guess = await self.bot.wait_for('message', timeout=15.0, check=check)
            
            if int(guess.content) == answer:
                win_embed = discord.Embed(
                    title="Correct! 🎉",
                    description=f"The answer was {answer}",
                    color=self.bot.colors['success']
                )
                await ctx.send(embed=win_embed)
            else:
                lose_embed = discord.Embed(
                    title="Wrong! ❌",
                    description=f"The correct answer was {answer}",
                    color=self.bot.colors['error']
                )
                await ctx.send(embed=lose_embed)
                
        except asyncio.TimeoutError:
            timeout_embed = discord.Embed(
                title="Time's Up!",
                description=f"The answer was {answer}",
                color=self.bot.colors['error']
            )
            await ctx.send(embed=timeout_embed)

async def setup(bot):
    await bot.add_cog(MathGame(bot))

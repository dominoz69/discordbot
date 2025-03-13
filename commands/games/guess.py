import discord
from discord.ext import commands
import random
import asyncio

class NumberGuess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def guess(self, ctx, max_number: int = 100):
        """Guess a number between 1 and the specified maximum (default 100)"""
        number = random.randint(1, max_number)
        guesses = 0
        max_guesses = len(str(max_number)) + 2  # Dynamic max guesses based on number size
        
        embed = discord.Embed(
            title="Number Guessing Game",
            description=f"I'm thinking of a number between 1 and {max_number}.\nYou have {max_guesses} guesses!",
            color=self.bot.colors['primary']
        )
        message = await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()
            
        while guesses < max_guesses:
            try:
                guess_msg = await self.bot.wait_for("message", timeout=30.0, check=check)
                guess = int(guess_msg.content)
                guesses += 1
                
                if guess == number:
                    win_embed = discord.Embed(
                        title="Congratulations!",
                        description=f"You got it in {guesses} guesses! The number was {number}.",
                        color=self.bot.colors['success']
                    )
                    await message.edit(embed=win_embed)
                    break
                    
                hint = "higher" if guess < number else "lower"
                embed = discord.Embed(
                    title="Number Guessing Game",
                    description=f"The number is {hint} than {guess}!\nGuesses remaining: {max_guesses - guesses}",
                    color=self.bot.colors['primary']
                )
                await message.edit(embed=embed)
                
                if guesses >= max_guesses:
                    lose_embed = discord.Embed(
                        title="Game Over!",
                        description=f"You ran out of guesses! The number was {number}.",
                        color=self.bot.colors['error']
                    )
                    await message.edit(embed=lose_embed)
                    
            except asyncio.TimeoutError:
                timeout_embed = discord.Embed(
                    title="Game Over!",
                    description="Game timed out due to inactivity",
                    color=self.bot.colors['error']
                )
                await message.edit(embed=timeout_embed)
                break

async def setup(bot):
    await bot.add_cog(NumberGuess(bot))

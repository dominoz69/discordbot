import discord
from discord.ext import commands
import random
import asyncio

class Hangman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.words = [
            "python", "discord", "programming", "computer", "algorithm",
            "database", "network", "server", "gaming", "developer"
        ]
        self.hangman_stages = [
            """```
               ___________
               |         |
               |         
               |        
               |        
               |
            ___|___```""",
            """```
               ___________
               |         |
               |         O
               |        
               |        
               |
            ___|___```""",
            """```
               ___________
               |         |
               |         O
               |         |
               |        
               |
            ___|___```""",
            """```
               ___________
               |         |
               |         O
               |        /|
               |        
               |
            ___|___```""",
            """```
               ___________
               |         |
               |         O
               |        /|\\
               |        
               |
            ___|___```""",
            """```
               ___________
               |         |
               |         O
               |        /|\\
               |        /
               |
            ___|___```""",
            """```
               ___________
               |         |
               |         O
               |        /|\\
               |        / \\
               |
            ___|___```"""
        ]
        
    @commands.command()
    async def hangman(self, ctx):
        """Play a game of Hangman"""
        word = random.choice(self.words)
        guessed = set()
        wrong_guesses = 0
        
        def make_display():
            return " ".join(letter if letter in guessed else "_" for letter in word)
            
        def make_embed():
            embed = discord.Embed(
                title="Hangman",
                color=self.bot.colors['primary']
            )
            embed.add_field(name="Word", value=make_display(), inline=False)
            embed.add_field(name="Guessed Letters", value=", ".join(sorted(guessed)) or "None", inline=False)
            embed.add_field(name="Hangman", value=self.hangman_stages[wrong_guesses], inline=False)
            return embed
            
        message = await ctx.send(embed=make_embed())
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and len(m.content) == 1
            
        while wrong_guesses < 6:
            try:
                guess_msg = await self.bot.wait_for("message", timeout=30.0, check=check)
                guess = guess_msg.content.lower()
                
                if guess in guessed:
                    await ctx.send("You already guessed that letter!", delete_after=3)
                    continue
                    
                guessed.add(guess)
                
                if guess not in word:
                    wrong_guesses += 1
                
                await message.edit(embed=make_embed())
                
                if all(letter in guessed for letter in word):
                    win_embed = discord.Embed(
                        title="Congratulations!",
                        description=f"You won! The word was: {word}",
                        color=self.bot.colors['success']
                    )
                    await message.edit(embed=win_embed)
                    break
                    
                if wrong_guesses >= 6:
                    lose_embed = discord.Embed(
                        title="Game Over!",
                        description=f"You lost! The word was: {word}",
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
    await bot.add_cog(Hangman(bot))

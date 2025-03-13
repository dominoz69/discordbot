import discord
from discord.ext import commands
import random
import asyncio

class WordScramble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.words = [
            "python", "discord", "coding", "gaming", "server",
            "computer", "keyboard", "monitor", "program", "developer",
            "software", "hardware", "network", "internet", "database"
        ]
        
    @commands.command()
    async def wordscramble(self, ctx):
        """Play a word scramble game"""
        word = random.choice(self.words)
        scrambled = list(word)
        random.shuffle(scrambled)
        scrambled = ''.join(scrambled)
        
        embed = discord.Embed(
            title="Word Scramble",
            description=f"Unscramble this word: **{scrambled}**\nYou have 30 seconds!",
            color=self.bot.colors['primary']
        )
        await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
            
        try:
            guess = await self.bot.wait_for('message', timeout=30.0, check=check)
            
            if guess.content.lower() == word:
                win_embed = discord.Embed(
                    title="Congratulations! 🎉",
                    description=f"You got it! The word was **{word}**",
                    color=self.bot.colors['success']
                )
                await ctx.send(embed=win_embed)
            else:
                lose_embed = discord.Embed(
                    title="Wrong! ❌",
                    description=f"The correct word was **{word}**",
                    color=self.bot.colors['error']
                )
                await ctx.send(embed=lose_embed)
                
        except asyncio.TimeoutError:
            timeout_embed = discord.Embed(
                title="Time's Up!",
                description=f"The word was **{word}**",
                color=self.bot.colors['error']
            )
            await ctx.send(embed=timeout_embed)

async def setup(bot):
    await bot.add_cog(WordScramble(bot))

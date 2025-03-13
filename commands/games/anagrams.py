import discord
from discord.ext import commands
import random
import asyncio

class Anagrams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_words = [
            "python", "discord", "gaming", "coding", "server",
            "computer", "program", "keyboard", "monitor", "developer",
            "software", "database", "network", "internet", "command"
        ]
        
    def get_subwords(self, word):
        """Return some valid sub-words that can be made from the letters"""
        # This is a simplified version. In a real implementation,
        # you'd want to use a dictionary to check valid words
        valid_words = []
        letters = list(word.lower())
        
        # Generate some basic sub-words (this is just an example)
        if 'a' in letters:
            valid_words.append('a')
        if 'i' in letters:
            valid_words.append('i')
        if 'on' in word.lower():
            valid_words.append('on')
        if 'in' in word.lower():
            valid_words.append('in')
        if 'at' in word.lower():
            valid_words.append('at')
            
        return valid_words
        
    @commands.command()
    async def anagrams(self, ctx, time_limit: int = 60):
        """Make as many words as you can from the given letters"""
        if time_limit < 30 or time_limit > 180:
            await ctx.send("Time limit must be between 30 and 180 seconds!")
            return
            
        word = random.choice(self.base_words).upper()
        letters = list(word)
        random.shuffle(letters)
        scrambled = ''.join(letters)
        
        valid_subwords = self.get_subwords(word)
        found_words = set()
        
        embed = discord.Embed(
            title="Anagrams Game",
            description=f"Make as many words as you can using these letters:\n**{scrambled}**\n\n"
                       f"Time remaining: {time_limit} seconds\n"
                       f"Words found: {len(found_words)}",
            color=self.bot.colors['primary']
        )
        message = await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
            
        end_time = asyncio.get_event_loop().time() + time_limit
        
        while True:
            try:
                time_left = max(0, int(end_time - asyncio.get_event_loop().time()))
                if time_left == 0:
                    raise asyncio.TimeoutError
                    
                guess = await self.bot.wait_for('message', timeout=time_left, check=check)
                word_attempt = guess.content.lower()
                
                if word_attempt in found_words:
                    await ctx.send("You already found that word!", delete_after=2)
                    continue
                    
                if word_attempt in valid_subwords or word_attempt == word.lower():
                    found_words.add(word_attempt)
                    embed = discord.Embed(
                        title="Anagrams Game",
                        description=f"Letters: **{scrambled}**\n\n"
                                   f"Time remaining: {time_left} seconds\n"
                                   f"Words found: {len(found_words)}\n"
                                   f"Your words: {', '.join(sorted(found_words))}",
                        color=self.bot.colors['primary']
                    )
                    await message.edit(embed=embed)
                    
            except asyncio.TimeoutError:
                final_embed = discord.Embed(
                    title="Time's Up!",
                    description=f"Game Over!\n\n"
                               f"Original word: {word}\n"
                               f"You found {len(found_words)} words:\n"
                               f"{', '.join(sorted(found_words))}",
                    color=self.bot.colors['success']
                )
                await message.edit(embed=final_embed)
                break

async def setup(bot):
    await bot.add_cog(Anagrams(bot))

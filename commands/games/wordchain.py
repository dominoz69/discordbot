import discord 
from discord.ext import commands
import asyncio
import random

class WordChain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.words_used = {}  # Store used words per game
        
    @commands.command()
    async def wordchain(self, ctx, time_limit: int = 30):
        """Start a word chain game. Players must say words starting with the last letter of previous word"""
        if time_limit < 10 or time_limit > 60:
            await ctx.send("Time limit must be between 10 and 60 seconds!")
            return
            
        embed = discord.Embed(
            title="Word Chain Game",
            description=f"Game starting! Say a word within {time_limit} seconds.\nWords can't be repeated!",
            color=self.bot.colors['primary']
        )
        await ctx.send(embed=embed)
        
        self.words_used[ctx.channel.id] = set()
        last_word = None
        current_player = ctx.author
        
        def check(m):
            return m.channel == ctx.channel and not m.author.bot
            
        while True:
            try:
                message = await self.bot.wait_for("message", timeout=time_limit, check=check)
                word = message.content.lower().strip()
                
                # Validate word
                if len(word) < 2:
                    continue
                    
                if word in self.words_used[ctx.channel.id]:
                    await ctx.send(f"{message.author.mention} that word has already been used!", delete_after=3)
                    continue
                    
                if last_word and word[0] != last_word[-1]:
                    await ctx.send(f"{message.author.mention} your word must start with '{last_word[-1]}'!", delete_after=3)
                    continue
                    
                self.words_used[ctx.channel.id].add(word)
                last_word = word
                current_player = message.author
                
                embed = discord.Embed(
                    title="Word Chain",
                    description=f"Current word: **{word}**\nNext word must start with: **{word[-1]}**",
                    color=self.bot.colors['secondary']
                )
                embed.set_footer(text=f"Current player: {current_player.name}")
                await ctx.send(embed=embed)
                
            except asyncio.TimeoutError:
                if not last_word:
                    description = "Game ended - no words were played!"
                else:
                    description = f"Time's up! Last word was: **{last_word}**\nLast player: {current_player.mention}"
                    
                embed = discord.Embed(
                    title="Game Over!",
                    description=description,
                    color=self.bot.colors['error']
                )
                embed.add_field(name="Words Used", value=str(len(self.words_used[ctx.channel.id])))
                await ctx.send(embed=embed)
                del self.words_used[ctx.channel.id]
                break

async def setup(bot):
    await bot.add_cog(WordChain(bot))

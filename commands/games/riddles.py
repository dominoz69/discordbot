import discord
from discord.ext import commands
import random
import asyncio

class Riddles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.riddles = [
            {
                'question': "What has keys, but no locks; space, but no room; and you can enter, but not go in?",
                'answer': 'keyboard',
                'hint': "You're using it to type"
            },
            {
                'question': "What gets wetter and wetter the more it dries?",
                'answer': 'towel',
                'hint': "You use it after a shower"
            },
            {
                'question': "What has legs, but doesn't walk?",
                'answer': 'table',
                'hint': "You eat on it"
            },
            {
                'question': "What has many keys but no locks, many spaces but no room?",
                'answer': 'piano',
                'hint': "It makes music"
            },
            {
                'question': "The more you take, the more you leave behind. What am I?",
                'answer': 'footsteps',
                'hint': "You make these when you walk"
            }
        ]
        
    @commands.command()
    async def riddle(self, ctx):
        """Play a riddle game! Try to solve the riddle with optional hints"""
        riddle = random.choice(self.riddles)
        
        embed = discord.Embed(
            title="Riddle Game",
            description=f"{riddle['question']}\n\nReact with 💡 for a hint or type your answer!",
            color=self.bot.colors['primary']
        )
        message = await ctx.send(embed=embed)
        await message.add_reaction('💡')
        
        def check_message(m):
            return m.author == ctx.author and m.channel == ctx.channel
            
        def check_reaction(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '💡'
            
        hint_used = False
        while True:
            try:
                done, pending = await asyncio.wait([
                    self.bot.wait_for('message', timeout=30.0, check=check_message),
                    self.bot.wait_for('reaction_add', timeout=30.0, check=check_reaction)
                ], return_when=asyncio.FIRST_COMPLETED)
                
                try:
                    stuff = done.pop().result()
                    
                    for future in pending:
                        future.cancel()
                        
                    if isinstance(stuff, discord.Message):
                        # Handle answer
                        if stuff.content.lower() == riddle['answer']:
                            win_embed = discord.Embed(
                                title="Correct! 🎉",
                                description=f"You solved the riddle!",
                                color=self.bot.colors['success']
                            )
                            await ctx.send(embed=win_embed)
                            break
                        else:
                            await ctx.send("That's not correct! Try again!", delete_after=2)
                    else:
                        # Handle hint
                        if not hint_used:
                            hint_embed = discord.Embed(
                                title="Hint",
                                description=riddle['hint'],
                                color=self.bot.colors['secondary']
                            )
                            await ctx.send(embed=hint_embed)
                            hint_used = True
                            await message.remove_reaction('💡', ctx.author)
                        
                except asyncio.TimeoutError:
                    break
                    
            except asyncio.TimeoutError:
                timeout_embed = discord.Embed(
                    title="Time's Up!",
                    description=f"The answer was: {riddle['answer']}",
                    color=self.bot.colors['error']
                )
                await ctx.send(embed=timeout_embed)
                break

async def setup(bot):
    await bot.add_cog(Riddles(bot))

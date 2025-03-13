import discord
from discord.ext import commands
import asyncio
import random

class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.questions = {
            'python': [
                {
                    'question': 'What function is used to get the length of a list?',
                    'answer': 'len',
                    'options': ['length', 'len', 'size', 'count']
                },
                {
                    'question': 'Which keyword is used for functions?',
                    'answer': 'def',
                    'options': ['def', 'function', 'fun', 'define']
                }
            ],
            'gaming': [
                {
                    'question': 'Which game features a character named Master Chief?',
                    'answer': 'halo',
                    'options': ['doom', 'halo', 'destiny', 'gears']
                },
                {
                    'question': 'What company makes the PlayStation?',
                    'answer': 'sony',
                    'options': ['microsoft', 'nintendo', 'sony', 'sega']
                }
            ]
        }
        
    @commands.command()
    async def trivia(self, ctx, category: str = None):
        """Play a trivia game! Categories: python, gaming"""
        if category and category.lower() not in self.questions:
            categories = ', '.join(self.questions.keys())
            await ctx.send(f"Invalid category! Available categories: {categories}")
            return
            
        if not category:
            category = random.choice(list(self.questions.keys()))
            
        question_data = random.choice(self.questions[category])
        options = question_data['options']
        correct_answer = question_data['answer']
        
        # Create embed with question
        embed = discord.Embed(
            title=f"Trivia - {category.capitalize()}",
            description=question_data['question'],
            color=self.bot.colors['primary']
        )
        
        for i, option in enumerate(options):
            embed.add_field(name=f"Option {i+1}", value=option, inline=True)
            
        message = await ctx.send(embed=embed)
        
        # Add reaction options
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
        for reaction in reactions:
            await message.add_reaction(reaction)
            
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in reactions
            
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            
            selected_index = reactions.index(str(reaction.emoji))
            selected_answer = options[selected_index]
            
            if selected_answer.lower() == correct_answer.lower():
                result_embed = discord.Embed(
                    title="Correct! 🎉",
                    description=f"The answer was: {correct_answer}",
                    color=self.bot.colors['success']
                )
            else:
                result_embed = discord.Embed(
                    title="Wrong! ❌",
                    description=f"The correct answer was: {correct_answer}",
                    color=self.bot.colors['error']
                )
                
            await message.edit(embed=result_embed)
            
        except asyncio.TimeoutError:
            timeout_embed = discord.Embed(
                title="Time's Up!",
                description=f"The correct answer was: {correct_answer}",
                color=self.bot.colors['error']
            )
            await message.edit(embed=timeout_embed)

async def setup(bot):
    await bot.add_cog(Trivia(bot))

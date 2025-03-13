import discord
from discord.ext import commands
import random
import asyncio

class CoinFlip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coins = {
            'heads': '🪙 Heads',
            'tails': '💫 Tails'
        }
        
    @commands.command(aliases=['flip', 'coin'])
    async def coinflip(self, ctx, bet: str = None):
        """Flip a coin! Optionally bet on heads or tails"""
        result = random.choice(['heads', 'tails'])
        
        if bet:
            bet = bet.lower()
            if bet not in ['heads', 'tails']:
                await ctx.send("Please bet on either 'heads' or 'tails'!")
                return
                
            embed = discord.Embed(
                title="Coin Flip",
                description="Flipping the coin...",
                color=self.bot.colors['primary']
            )
            message = await ctx.send(embed=embed)
            
            await asyncio.sleep(1)  # Add suspense
            
            if bet == result:
                description = f"It's {self.coins[result]}!\nYou won! 🎉"
                color = self.bot.colors['success']
            else:
                description = f"It's {self.coins[result]}!\nYou lost! 😢"
                color = self.bot.colors['error']
                
        else:
            description = f"It's {self.coins[result]}!"
            color = self.bot.colors['secondary']
            message = None
            
        embed = discord.Embed(
            title="Coin Flip",
            description=description,
            color=color
        )
        
        if message:
            await message.edit(embed=embed)
        else:
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CoinFlip(bot))

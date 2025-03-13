import discord
from discord.ext import commands
from database import get_pool
import logging

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def ping(self, ctx):
        """Check bot's latency"""
        embed = discord.Embed(
            title="Pong! 🏓",
            description=f"Latency: {round(self.bot.latency * 1000)}ms",
            color=self.bot.colors['primary']
        )
        await ctx.send(embed=embed)
        
    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        """Get information about a user"""
        member = member or ctx.author
        
        async with await get_pool() as pool:
            user = await pool.fetchrow(
                'SELECT * FROM users WHERE user_id = $1',
                member.id
            )
            
            if not user:
                await pool.execute(
                    'INSERT INTO users (user_id, username) VALUES ($1, $2)',
                    member.id, str(member)
                )
        
        embed = discord.Embed(
            title="User Information",
            color=self.bot.colors['secondary']
        )
        embed.add_field(name="Name", value=str(member), inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Joined At", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))

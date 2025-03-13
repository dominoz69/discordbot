import discord
from discord.ext import commands
import logging

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a member from the server"""
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="Member Kicked",
            description=f"{member.mention} has been kicked\nReason: {reason}",
            color=self.bot.colors['error']
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Kick(bot))

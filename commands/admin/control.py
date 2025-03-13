import discord
from discord.ext import commands
import sys
import os
import asyncio

class BotControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """Check if user is the bot admin"""
        return self.bot.is_admin(ctx.author.id)

    @commands.command()
    async def restart(self, ctx):
        """Restart the bot (Admin only)"""
        embed = discord.Embed(
            title="Bot Restart",
            description="Restarting bot...",
            color=self.bot.colors['primary']
        )
        await ctx.send(embed=embed)
        await self.bot.close()
        os.execv(sys.executable, ['python'] + sys.argv)

    @commands.command()
    async def shutdown(self, ctx):
        """Shutdown the bot (Admin only)"""
        embed = discord.Embed(
            title="Bot Shutdown",
            description="Shutting down...",
            color=self.bot.colors['error']
        )
        await ctx.send(embed=embed)
        await self.bot.close()

    @commands.command()
    async def leaveserver(self, ctx):
        """Make the bot leave the server (Admin only)"""
        embed = discord.Embed(
            title="Leave Server",
            description="Are you sure you want me to leave this server? React with ✅ to confirm.",
            color=self.bot.colors['error']
        )
        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅'

        try:
            await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            await ctx.guild.leave()
        except asyncio.TimeoutError:
            await message.edit(embed=discord.Embed(
                title="Leave Server",
                description="Command timed out.",
                color=self.bot.colors['secondary']
            ))

async def setup(bot):
    await bot.add_cog(BotControl(bot))
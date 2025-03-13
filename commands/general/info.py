import discord
from discord.ext import commands
import datetime
import psutil
import os

class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()
        
    @commands.command()
    async def uptime(self, ctx):
        """Show bot's uptime"""
        current_time = datetime.datetime.utcnow()
        uptime = current_time - self.start_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        embed = discord.Embed(
            title="Bot Uptime",
            description=f"Online for: {days}d {hours}h {minutes}m {seconds}s",
            color=self.bot.colors['primary']
        )
        await ctx.send(embed=embed)
        
    @commands.command()
    async def status(self, ctx):
        """Show bot's current status"""
        embed = discord.Embed(
            title="Bot Status",
            color=self.bot.colors['primary']
        )
        
        # System info
        process = psutil.Process(os.getpid())
        mem = process.memory_info()
        
        embed.add_field(name="Memory Usage", value=f"{mem.rss / 1024 / 1024:.2f} MB", inline=True)
        embed.add_field(name="CPU Usage", value=f"{psutil.cpu_percent()}%", inline=True)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Servers", value=str(len(self.bot.guilds)), inline=True)
        embed.add_field(name="Users", value=str(len(self.bot.users)), inline=True)
        embed.add_field(name="Commands", value=str(len(self.bot.commands)), inline=True)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BotInfo(bot))

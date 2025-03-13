import discord
from discord.ext import commands
import logging

class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Handle bot ready event"""
        logging.info(f'Logged in as {self.bot.user.name}')

        # Set bot status
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{self.bot.config['PREFIX']}help for commands"
        )
        await self.bot.change_presence(activity=activity)

async def setup(bot):
    await bot.add_cog(Ready(bot))
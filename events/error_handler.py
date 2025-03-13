import discord
from discord.ext import commands
import logging
from utils.formatting import format_error

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Handle command errors"""
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Error",
                description="You don't have permission to use this command",
                color=self.bot.colors['error']
            )
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                title="Error",
                description="Member not found",
                color=self.bot.colors['error']
            )
        else:
            logging.error(f"Command error: {str(error)}")
            embed = discord.Embed(
                title="Error",
                description=format_error(error),
                color=self.bot.colors['error']
            )
            
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))

import discord
from discord.ext import commands
import logging
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

logger = logging.getLogger('discord_bot')

class MemberEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Handle member join event"""
        try:
            logger.info(f"{Fore.GREEN}New member joined: {member.name}#{member.discriminator}")

            # Send welcome message
            welcome_channel = discord.utils.get(member.guild.text_channels, name='welcome')
            if welcome_channel:
                embed = discord.Embed(
                    title=f"Welcome to {member.guild.name}! 👋",
                    description=f"Welcome {member.mention}! Please read the rules below:",
                    color=self.bot.colors['success']
                )

                # Add server rules
                rules = [
                    "Be respectful to all members",
                    "No spam or self-promotion",
                    "Keep discussions in appropriate channels",
                    "Follow Discord's Terms of Service",
                    "Listen to and respect staff members"
                ]

                rules_text = "\n".join(f"📜 {i+1}. {rule}" for i, rule in enumerate(rules))
                embed.add_field(name="Server Rules", value=rules_text, inline=False)

                await welcome_channel.send(embed=embed)
        except Exception as e:
            logger.error(f"{Fore.RED}Error in member_join event: {str(e)}{Style.RESET_ALL}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Handle member leave event"""
        try:
            logger.info(f"{Fore.YELLOW}Member left: {member.name}#{member.discriminator}")

            # Send leave message
            log_channel = discord.utils.get(member.guild.text_channels, name='member-logs')
            if log_channel:
                embed = discord.Embed(
                    title="Member Left",
                    description=f"{member.mention} has left the server",
                    color=self.bot.colors['error']
                )
                await log_channel.send(embed=embed)
        except Exception as e:
            logger.error(f"{Fore.RED}Error in member_remove event: {str(e)}{Style.RESET_ALL}")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        """Handle member ban event"""
        try:
            logger.info(f"{Fore.RED}Member banned: {user.name}#{user.discriminator}")

            # Send ban message
            log_channel = discord.utils.get(guild.text_channels, name='mod-logs')
            if log_channel:
                embed = discord.Embed(
                    title="Member Banned",
                    description=f"{user.mention} has been banned from the server",
                    color=self.bot.colors['error']
                )
                await log_channel.send(embed=embed)
        except Exception as e:
            logger.error(f"{Fore.RED}Error in member_ban event: {str(e)}{Style.RESET_ALL}")

    @commands.Cog.listener()
    async def on_member_kick(self, guild, user):
        """Handle member kick event"""
        try:
            logger.info(f"{Fore.RED}Member kicked: {user.name}#{user.discriminator}")

            # Send kick message
            log_channel = discord.utils.get(guild.text_channels, name='mod-logs')
            if log_channel:
                embed = discord.Embed(
                    title="Member Kicked",
                    description=f"{user.mention} has been kicked from the server",
                    color=self.bot.colors['error']
                )
                await log_channel.send(embed=embed)
        except Exception as e:
            logger.error(f"{Fore.RED}Error in member_kick event: {str(e)}{Style.RESET_ALL}")

async def setup(bot):
    await bot.add_cog(MemberEvents(bot))
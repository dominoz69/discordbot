import os
import discord
from discord.ext import commands
import logging
from config import load_config
import asyncio
import glob
from colorama import Fore, Style

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord_bot')

class CustomHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="Bot Commands",
            description=f"Use `{self.context.clean_prefix}help <command>` for more info on a command.",
            color=self.context.bot.colors['primary']
        )

        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                cog_name = getattr(cog, "qualified_name", "No Category")
                command_list = []
                for cmd in filtered:
                    desc = cmd.help or "No description available"
                    command_list.append(f"`{self.context.clean_prefix}{cmd.name}` - {desc}")

                if command_list:
                    embed.add_field(
                        name=f"📚 {cog_name}",
                        value="\n".join(command_list),
                        inline=False
                    )

        await self.context.channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(
            title=f"Command: {command.name}",
            description=command.help or "No description available",
            color=self.context.bot.colors['primary']
        )

        if command.aliases:
            embed.add_field(name="Aliases", value=", ".join(f"`{a}`" for a in command.aliases))

        usage = f"`{self.context.clean_prefix}{command.name}`"
        if command.signature:
            usage += f" `{command.signature}`"
        embed.add_field(name="Usage", value=usage, inline=False)

        await self.context.channel.send(embed=embed)

class DiscordBot(commands.Bot):
    def __init__(self, config):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix=config['PREFIX'],
            intents=intents,
            help_command=CustomHelpCommand()
        )

        self.config = config
        self.colors = {
            'primary': 0x5865F2,    # Discord Blurple
            'secondary': 0x36393F,  # Discord Dark
            'success': 0x57F287,    # Discord Green
            'error': 0xED4245,      # Discord Red
        }

    async def setup_hook(self):
        # Load all command modules
        logger.info(f"{Fore.CYAN}Loading commands...{Style.RESET_ALL}")
        for command_file in glob.glob("commands/**/*.py", recursive=True):
            if not command_file.endswith('__init__.py'):
                module_path = command_file.replace('/', '.').replace('\\', '.')[:-3]
                try:
                    await self.load_extension(module_path)
                    logger.info(f"{Fore.GREEN}Loaded extension: {module_path}{Style.RESET_ALL}")
                except Exception as e:
                    logger.error(f"{Fore.RED}Failed to load extension {module_path}: {e}{Style.RESET_ALL}")

        # Load events
        logger.info(f"{Fore.CYAN}Loading events...{Style.RESET_ALL}")
        for event_file in ['events.error_handler', 'events.ready', 'events.member_events']:
            try:
                await self.load_extension(event_file)
                logger.info(f"{Fore.GREEN}Loaded event: {event_file}{Style.RESET_ALL}")
            except Exception as e:
                logger.error(f"{Fore.RED}Failed to load event {event_file}: {e}{Style.RESET_ALL}")

    def is_admin(self, user_id):
        """Check if a user is the bot admin"""
        return str(user_id) == str(self.config['admin']['id'])

if __name__ == "__main__":
    # Load configuration
    config = load_config()

    # Create bot instance
    bot = DiscordBot(config)

    # Start the bot
    asyncio.run(bot.start(config['discord_token']))

import os
import json
from dotenv import load_dotenv

def load_config():
    """Load configuration from config files and environment variables"""
    load_dotenv()

    config = {
        'MONGO_URI': os.getenv('MONGO_URI', ''),
        'PREFIX': os.getenv('BOT_PREFIX', '@'),
        'admin': {
            'id': os.getenv('ADMIN_ID', '1328664549733433369')
        }
    }

    # Get Discord token from environment variable
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError("Discord token not found. Please set DISCORD_TOKEN environment variable")

    config['discord_token'] = token

    return config
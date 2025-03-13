# Discord Bot Setup Guide

This guide will help you set up and configure your Discord bot using environment variables for secure configuration management.

## Environment Variables

Your bot uses the following environment variables:

- `TOKEN`: Your Discord bot's authentication token
- `PREFIX`: Command prefix for your bot (e.g., `!`, `.`, `$`)
- `ADMIN`: Discord user ID of the bot administrator
- `MONGO_URI`: Connection string for your MongoDB database

## Create a `.env` File

Create a file named `.env` in the root directory of your project:

```
TOKEN=your_discord_bot_token_here
PREFIX=!
ADMIN=your_discord_user_id
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/database
```


## How to Get a Discord Bot Token

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Navigate to the "Bot" tab in the left sidebar
4. Click "Add Bot" and confirm
5. Under the "TOKEN" section, click "Copy" to copy your bot token
   - Keep this token secret! Anyone with this token can control your bot
6. Toggle on the necessary "Privileged Gateway Intents" (Message Content, Server Members, Presence)

## Adding Your Bot to a Discord Server

1. Still in the Discord Developer Portal, go to the "OAuth2" tab in the left sidebar
2. Click on "URL Generator"
3. Under "Scopes," select "bot" and "applications.commands"
4. Under "Bot Permissions," select the permissions your bot needs:
   - Basic permissions: Send Messages, Read Message History, Embed Links
   - Additional permissions based on your bot's functionality
5. Copy the generated URL at the bottom of the page
6. Paste the URL in your web browser
7. Select the server where you want to add the bot
8. Click "Authorize"
9. Complete the CAPTCHA verification if prompted

## Connecting to MongoDB

1. Sign up for a [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account
2. Create a new cluster (the free tier is sufficient for most small bots)
3. Click "Connect" on your cluster
4. Select "Connect your application"
5. Copy the connection string
6. Replace `<username>`, `<password>`, and `<dbname>` with your MongoDB username, password, and database name
7. Paste this URI into your `.env` file as the `MONGO_URI` value

## Running Your Bot

With the environment variables configured, you can now run your bot:

```bash
python main.py
```

## Security Best Practices

- Never commit your `.env` file to version control (add it to your `.gitignore`)
- Regularly rotate your bot token for enhanced security
- Use restricted MongoDB user permissions
- Keep your bot's dependencies updated
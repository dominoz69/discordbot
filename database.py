import motor.motor_asyncio
import os
import logging
from dotenv import load_dotenv

load_dotenv()

async def init_db():
    mongo_uri = os.getenv('MONGO_URI')

    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
        db = client.get_default_database()

        collection_names = await db.list_collection_names()
        if 'users' not in collection_names:
            await db.create_collection('users')

        logging.info("Database initialized successfully")
        return client

    except Exception as e:
        logging.error(f"Database initialization failed: {str(e)}")
        raise

async def get_db():
    mongo_uri = os.getenv('MONGO_URI')

    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
    return client.get_default_database()
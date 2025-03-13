import asyncpg
import os
import logging
from config import load_config

async def init_db():
    """Initialize database connection and create tables if they don't exist"""
    config = load_config()['database']
    
    try:
        conn = await asyncpg.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password']
        )
        
        # Create tables
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        await conn.close()
        logging.info("Database initialized successfully")
        
    except Exception as e:
        logging.error(f"Database initialization failed: {str(e)}")
        raise

async def get_pool():
    """Get connection pool for database operations"""
    config = load_config()['database']
    
    return await asyncpg.create_pool(
        host=config['host'],
        port=config['port'],
        database=config['database'],
        user=config['user'],
        password=config['password']
    )

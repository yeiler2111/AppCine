import os
from redis import asyncio as aioredis
from dotenv import load_dotenv

load_dotenv()

class RedisClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "client"):
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
            self.client = aioredis.from_url(redis_url, decode_responses=True)

    def get_client(self):
        return self.client


redis_instance = RedisClient()

from flask_sqlalchemy import SQLAlchemy
import redis
import os
from dotenv import load_dotenv

load_dotenv()

redis_password= os.getenv("REDIS_PASSWORD")
redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT", 6379))


db = SQLAlchemy()

try:
    redis_client = redis.Redis(host = redis_host, port = redis_port, password = redis_password, decode_responses=True)
    redis_client.ping()
except redis.ConnectionError:
    print("⚠️ Redis server not available! Ensure Redis is running.")

# redis_client = redis.from_url(os.getenv("REDIS_HOST"), 
#                                password=redis_password, 
#                                port=redis_port, 
#                                decode_responses=True)


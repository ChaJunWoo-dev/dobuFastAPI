import redis
from starlette.config import Config

config = Config(".env")

REDIS_PORT = config("REDIS_PORT")
REDIS_HOST = config("REDIS_HOST")
REDIS_PASSWORD = config("REDIS_PASSWORD")

rd = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

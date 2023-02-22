from redis.client import Redis

from core.config import settings

redis_conn = Redis(
    host=settings.REDIS_SERVER, port=settings.REDIS_PORT, db=0, decode_responses=True
)
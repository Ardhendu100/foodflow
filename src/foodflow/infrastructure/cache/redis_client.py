# Only responsible for connecting Redis
import redis

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)

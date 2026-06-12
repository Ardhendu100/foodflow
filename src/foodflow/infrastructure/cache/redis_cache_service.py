import json

from foodflow.infrastructure.cache.cache_service import (
    CacheService,
)

from foodflow.infrastructure.cache.redis_client import (
    redis_client,
)


# We use json as redis stor in strings but our data is Python objects so we used dumps and loads
class RedisCacheService(CacheService):
    def get(
        self,
        key: str,
    ):
        value = redis_client.get(key)

        if value:
            return json.loads(value)

        return None

    def set(
        self,
        key: str,
        value,
        ttl: int | None = None,
    ):
        serialized = json.dumps(value)

        if ttl:
            redis_client.setex(
                key,
                ttl,
                serialized,
            )
        else:
            redis_client.set(
                key,
                serialized,
            )

    def delete(
        self,
        key: str,
    ):
        redis_client.delete(key)

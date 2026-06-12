from foodflow.infrastructure.cache.redis_cache_service import (
    RedisCacheService,
)


class CacheFactory:
    @staticmethod
    def get_cache():
        return RedisCacheService()

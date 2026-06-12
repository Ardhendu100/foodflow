# It defines what operations a cache must support, this file says the opeartions not saying Use Redis, or Use memory or Use Memcached
from abc import ABC, abstractmethod


class CacheService(ABC):
    @abstractmethod
    def get(
        self,
        key: str,
    ):
        pass

    @abstractmethod
    def set(
        self,
        key: str,
        value: str,
        ttl: int | None = None,
    ):
        pass

    @abstractmethod
    def delete(
        self,
        key: str,
    ):
        pass

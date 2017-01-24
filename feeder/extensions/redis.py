"""extensions redis."""
from redis import StrictRedis, ConnectionPool


class RedisBackend(object):

    def __init__(self, **kwargs):
        pool = ConnectionPool(**kwargs)
        self._kvstore = StrictRedis(connection_pool=pool)

    # pylint: disable=C0103
    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        return self._kvstore.set(name, value, ex, px, nx, xx)

    def scard(self, name):
        return self._kvstore.scard(name)

    def sadd(self, name, *values):
        return self._kvstore.sadd(name, *values)

    def smembers(self, name):
        """Return all members of the set name."""
        return {item.decode() for item in self._kvstore.smembers(name)}

    def sismember(self, name, value):
        """Return a boolean indicating if value is a member of set name."""
        return self._kvstore.sismember(name, value)

    def get(self, name):
        if self.exists(name):
            return self._kvstore.get(name).decode()
        return self._kvstore.get(name)

    def incr(self, name, ex=None):
        result = self._kvstore.incr(name)

        if result and ex:
            self.expire(name, ex)
        return result

    def expire(self, name, time):
        return self._kvstore.expire(name, time)

    def flushall(self):
        """Delete all keys in all databases on the current host."""
        return self._kvstore.flushall()

    def flushdb(self):
        """Delete all keys in the current database."""
        return self._kvstore.flushdb()

    def delete(self, name):
        return self._kvstore.delete(name)

    def exists(self, name):
        return self._kvstore.exists(name)

    def keys(self, pattern='*'):
        return self._kvstore.keys(pattern)

    def rpush(self, name, *values):
        return self._kvstore.rpush(name, *values)

    def lpop(self, name):
        retdata = self._kvstore.lpop(name)
        if retdata:
            retdata = retdata.decode()
        return retdata

    def llen(self, name):
        return self._kvstore.llen(name)

    def lrange(self, name, start, end):
        lst = self._kvstore.lrange(name, start, end)
        retdata = [i.decode() for i in lst]
        return retdata

    def lrem(self, name, count, value):
        """
        Remove the first ``count`` occurrences of elements equal to ``value``
        from the list stored at ``name``.
        """
        return self._kvstore.lrem(name, count, value)

    def hincrby(self, name, key, amount=1):
        return self._kvstore.hincrby(name, key, amount=amount)

    def hset(self, name, key, value):
        result = self._kvstore.hset(name, key, value)
        if isinstance(result, bytes):
            result = result.decode()
        return result

    def hexists(self, name, key):
        return self._kvstore.hexists(name, key)

    def hget(self, name, key):
        result = self._kvstore.hget(name, key)
        if result:
            result = result.decode()
        return result

    def hgetall(self, name):
        result = self._kvstore.hgetall(name)
        result = {key.decode(): value.decode()
                  for key, value in result.items()}
        return result


REDIS_CONFIG = {
    'host': '127.0.0.1',
    'port': '6379',
    'db': '6'
}

KVSTORE = RedisBackend(**REDIS_CONFIG)

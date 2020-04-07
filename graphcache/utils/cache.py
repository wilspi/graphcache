import string
import random
import redis
import pickle


class Cache:
    """
    Cache class

    """

    def __init__(self, host="localhost", port=6379, db=0):
        # Redis client
        try:
            self.host = host
            self.port = port
            self.db = db
            self.cache = redis.StrictRedis(host=self.host, port=self.port, db=self.db)
        except Exception:
            raise Exception("Cache Error: Failed to connect to server")

    def get_random_key(self, size=6, chars=string.ascii_uppercase + string.digits):
        """
        Get random key

        Parameters
        ----------
        size: int
        chars: string

        Returns
        -------
        string
        """

        return "graphcache-" + ("".join(random.choice(chars) for _ in range(size)))

    def set(self, key, value, ttl=None):
        """
        Set key-value pair in cache

        Parameters
        ----------
        key: string
        value: any data type
        ttl: int

        Returns
        -------
        string
        """

        if ttl is None:
            self.cache.set(key, pickle.dumps(value))

        elif ttl > 0:
            self.cache.set(key, pickle.dumps(value), ex=ttl)

        else:
            raise Exception("Value Error: TTL must be positive")

        return key

    def get(self, key, silent=False):
        """
        Get value by key from cache

        Parameters
        ----------
        key: string
        silent: bool

        Returns
        -------
        any type
            value of any type, which was stored
        """

        try:
            value_obj = self.cache.get(key)
            if value_obj is None:
                raise Exception("Value not found")
            value = pickle.loads(value_obj)
            if value.__class__.__name__ in ("GraphCache", "Node", "NodeRef"):
                value.cache = self

        except Exception:
            if silent:
                return None
            raise Exception("Cache Exception: " + key + " is not found")

        return value

    def remove(self, key):
        """
        Remove key-value pair from cache

        Parameters
        ----------
        key: string
        """

        try:
            self.cache.delete(key)

        except Exception:
            pass

    def __getstate__(self):
        """
        Required for pickling, since can't pickle redis connection
        """
        return {"host": self.host, "port": self.port, "db": self.db}

    def __setstate__(self, d):
        """
        Required for pickling, since can't pickle redis connection
        """
        self.__dict__ = d
        self.__dict__["cache"] = redis.StrictRedis(
            host=d["host"], port=d["port"], db=d["db"]
        )

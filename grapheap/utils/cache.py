import pylibmc
import string
import random
import sys
from os.path import expanduser

# Python version
if sys.version_info[0] < 3:
    from ConfigParser import ConfigParser # python 2
else:
    from configparser import ConfigParser # python 3


# Load configuration
# Get cache configuration from ~/grapheap_config.conf
Config = ConfigParser()
Config.read(expanduser("~") + '/grapheap_config.conf')
cache_servers = Config.get("Memcache", "cache_servers")
cache_servers = cache_servers[1:-1].split(',')



class Cache:
    """
    Cache class

    """

    # Global memcache client for this class
    try:
        cache = pylibmc.Client(
            cache_servers,
            binary=True,
            behaviors={"tcp_nodelay": True, "ketama": True})
    except Exception:
        raise Exception("Cache Error: Failed to connect to server")

    @staticmethod
    def get_random_key(size=6, chars=string.ascii_uppercase + string.digits):
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

        return 'grapheap-'+(''.join(random.choice(chars) for _ in range(size)))


    @staticmethod
    def set(key, value, ttl=None):
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
            Cache.cache.set(key, value)

        elif ttl > 0:
            Cache.cache.set(key, value, ttl)

        else:
            raise Exception("Value Error: TTL must be positive")

        return key

    @staticmethod
    def get(key, silent=False):
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
            value = Cache.cache[key]

        except Exception:
            if silent:
                return None
            raise Exception("Cache Exception: " + key + " is not found")

        return value

    @staticmethod
    def remove(key):
        """
        Remove key-value pair from cache

        Parameters
        ----------
        key: string
        """

        try:
            Cache.get(key)
            del Cache.cache[key]

        except Exception:
            pass

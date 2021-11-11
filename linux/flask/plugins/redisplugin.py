import redis
from config import redis_host
from config import redis_port
from config import redis_db
from functools import lru_cache

class Redis_Plugin:
    def __init__(self,passed_key,cache_value):
        self.passedkey = passed_key
        self.cache_value = cache_value

    @lru_cache(maxsize=100)
    def return_redis_cache(self):
        r = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
        if(r.exists(self.passedkey)):
            res = r.get(self.passedkey)
        else:
            res = False
        return res

    def insert_into_cache(self):
        if(self.cache_value is not None):
            r = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
            r.set(self.passedkey, self.cache_value)
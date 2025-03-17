import redis
from competencies.settings import REDIS_HOST, REDIS_PORT


def check_connect_redis():
    try:
        con = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        con.ping()
    except redis.exceptions.RedisError:
        return False
    return True

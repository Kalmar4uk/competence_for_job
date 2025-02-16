import redis
from competencies.settings import REDIS_HOST, REDIS_PORT
from matrix.models import Competence
from matrix.constants import CURRENT_DATE


def check_passing_date(user):
    return Competence.objects.filter(
            user=user,
            created_at__date=CURRENT_DATE
        )


def check_connect_redis():
    try:
        con = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        con.ping()
    except redis.exceptions.RedisError:
        return False
    return True

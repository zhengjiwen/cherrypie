import redis
import settings

pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
r = redis.Redis(connection_pool=pool)

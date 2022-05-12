import os


def get_sync_db_url():
    return 'postgresql://%s:%s@%s/%s' % (
        os.getenv('DB_USER', ''),
        os.getenv('DB_PASSWORD', ''),
        os.getenv('DB_HOST', 'localhost:5557'),
        os.getenv('DB_NAME', 'db'),
    )


def get_async_db_url():
    return 'postgresql+asyncpg://%s:%s@%s/%s' % (
        os.getenv('DB_USER', ''),
        os.getenv('DB_PASSWORD', ''),
        os.getenv('DB_HOST', 'localhost:5557'),
        os.getenv('DB_NAME', 'db'),
    )


def get_redis_url():
    return 'redis://%s:%s/%s' % (
        os.getenv('REDIS_HOST', 'localhost'),
        os.getenv('REDIS_PORT', '6379'),
        os.getenv('REDIS_DB', '1')
    )

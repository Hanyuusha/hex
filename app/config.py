import os


def get_db_url():
    return 'postgresql://%s:%s@%s/%s' % (
        os.getenv('DB_USER', ''),
        os.getenv('DB_PASSWORD', ''),
        os.getenv('DB_HOST', 'localhost:5557'),
        os.getenv('DB_NAME', 'db'),
    )

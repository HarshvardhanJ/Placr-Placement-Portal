import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-fallback-key")
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-fallback-key")
    CELERY = {
        "result_backend": os.environ.get(
            "CELERY_RESULT_BACKEND", "redis://redis:6379/0"
        ),
        "broker_url": os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0"),
        "task_serializer": "json",
        "result_serializer": "json",
        "accept_content": ["json"],
        "timezone": "Asia/Kolkata",
        "enable_utc": False,
    }

    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = os.environ.get("CACHE_REDIS_HOST", "redis")
    CACHE_REDIS_PORT = int(os.environ.get("CACHE_REDIS_PORT", 6379))
    CACHE_REDIS_DB = int(os.environ.get("CACHE_REDIS_DB", 2))
    CACHE_DEFAULT_TIMEOUT = 300

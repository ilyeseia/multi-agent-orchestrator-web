import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://orchestrator:secure_password_123@db:5432/orchestrator_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://redis:6379/0")

# utils/celery.py
from celery import Celery

celery_app = Celery(
    "orchestrator",
    broker="redis://redis:6379/0",  # عدّل حسب إعداداتك
    backend="redis://redis:6379/0"  # اختياري إذا تريد تتبع النتائج
)

celery_app.autodiscover_tasks(packages=["app.tasks"])  # عدّل المسار حسب مشروعك

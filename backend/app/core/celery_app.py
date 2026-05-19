from celery import Celery
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

celery = Celery(
    "worker",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL")
)

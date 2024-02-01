import json
import time

import psutil
from sqlalchemy import text

from .database import AsyncSessionLocal, SessionLocal


class HealthCheck:
    @staticmethod
    def check_sync_db() -> bool:
        try:
            with SessionLocal() as db:
                db.execute(text("SELECT 1"))
            return True
        except Exception:
            return False

    @staticmethod
    async def check_async_db() -> bool:
        try:
            async with AsyncSessionLocal() as db:
                await db.execute(text("SELECT 1"))
            return True
        except Exception:
            return False

    @classmethod
    async def check(cls) -> str:
        start_time = time.time()

        verifications = {
            "sync_db": cls.check_sync_db(),
            "async_db": await cls.check_async_db(),
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage("/").percent,
        }

        return json.dumps(
            {
                "status": "ok" if all(verifications.values()) else "fail",
                "verifications": verifications,
                "process_time_ms": round((time.time() - start_time) * 1000, 2),
            }
        )

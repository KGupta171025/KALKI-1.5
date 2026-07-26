import asyncio
import time
from typing import Dict, Any, Callable

class CronScheduler:
    """
    Schedules and dispatches tasks at designated intervals or CRON definitions.
    """
    def __init__(self):
        self.scheduled_jobs: Dict[str, Dict[str, Any]] = {}
        self.is_running = False

    def schedule_job(self, job_id: str, interval_seconds: int, callback: Callable, params: dict):
        self.scheduled_jobs[job_id] = {
            "interval": interval_seconds,
            "callback": callback,
            "params": params,
            "last_run": time.time()
        }
        print(f"[Scheduler] Job '{job_id}' registered with interval: {interval_seconds}s")

    async def start(self):
        self.is_running = True
        print("[Scheduler] Started background scheduling loop.")
        while self.is_running:
            current_time = time.time()
            for job_id, job in self.scheduled_jobs.items():
                if current_time - job["last_run"] >= job["interval"]:
                    job["last_run"] = current_time
                    asyncio.create_task(self._run_job(job_id, job))
            
            # Tick every 1 second
            await asyncio.sleep(1)

    async def _run_job(self, job_id: str, job: dict):
        print(f"[Scheduler] Triggering job: '{job_id}'")
        try:
            await job["callback"](job["params"])
        except Exception as e:
            print(f"[Scheduler ERROR] Job '{job_id}' failed: {str(e)}")

    def stop(self):
        self.is_running = False
        print("[Scheduler] Stopped scheduling loop.")

cron_scheduler = CronScheduler()

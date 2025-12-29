import schedule
import time
import threading
from datetime import datetime, timedelta
from typing import Callable, Dict, Any

from config.settings import SCHEDULE_SETTINGS
from utils.logger import logger


class Scheduler:
    """نظام جدولة المهام"""
    
    def __init__(self):
        self.jobs = {}
        self.running = False
        self.scheduler_thread = None
    
    def schedule_daily_task(self, task_name: str, task_func: Callable, 
                          schedule_time: str, *args, **kwargs) -> bool:
        """جدولة مهمة يومية"""
        
        try:
            # تحويل وقت الجدولة
            hour, minute = map(int, schedule_time.split(':'))
            
            # جدولة المهمة
            job = schedule.every().day.at(schedule_time).do(
                self._run_task_with_logging, task_name, task_func, *args, **kwargs
            )
            
            self.jobs[task_name] = job
            logger.info(f"Scheduled task '{task_name}' at {schedule_time}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error scheduling task '{task_name}': {e}")
            return False
    
    def schedule_short_tasks(self, task_func: Callable, *args, **kwargs):
        """جدولة الشورتات اليومية"""
        
        success_count = 0
        for i, schedule_time in enumerate(SCHEDULE_SETTINGS["shorts_schedule"]):
            task_name = f"short_{i+1}"
            if self.schedule_daily_task(task_name, task_func, schedule_time, *args, **kwargs):
                success_count += 1
        
        logger.info(f"Scheduled {success_count} out of {len(SCHEDULE_SETTINGS['shorts_schedule'])} short tasks")
        return success_count
    
    def schedule_compilation_task(self, task_func: Callable, *args, **kwargs):
        """جدولة مهمة الفيديو التجميعي"""
        
        task_name = "compilation"
        return self.schedule_daily_task(
            task_name, task_func, 
            SCHEDULE_SETTINGS["compilation_schedule"], 
            *args, **kwargs
        )
    
    def _run_task_with_logging(self, task_name: str, task_func: Callable, *args, **kwargs):
        """تشغيل المهمة مع تسجيل الأخطاء"""
        
        logger.info(f"Starting scheduled task: {task_name}")
        start_time = time.time()
        
        try:
            result = task_func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"Task '{task_name}' completed in {execution_time:.2f} seconds")
            return result
            
        except Exception as e:
            logger.error(f"Task '{task_name}' failed: {e}")
            # إعادة المحاولة بعد فترة
            self._retry_task(task_name, task_func, *args, **kwargs)
    
    def _retry_task(self, task_name: str, task_func: Callable, *args, **kwargs):
        """إعادة محاولة المهمة بعد فترة"""
        
        retry_delay = SCHEDULE_SETTINGS["retry_delay"]
        retry_attempts = SCHEDULE_SETTINGS["retry_attempts"]
        
        for attempt in range(retry_attempts):
            logger.info(f"Retrying task '{task_name}' (attempt {attempt + 1}) in {retry_delay} seconds")
            time.sleep(retry_delay)
            
            try:
                result = task_func(*args, **kwargs)
                logger.info(f"Task '{task_name}' succeeded on retry {attempt + 1}")
                return result
                
            except Exception as e:
                logger.error(f"Retry {attempt + 1} for task '{task_name}' failed: {e}")
        
        logger.error(f"Task '{task_name}' failed after {retry_attempts} retries")
    
    def start(self):
        """بدء تشغيل الجدولة"""
        
        if self.running:
            logger.warning("Scheduler is already running")
            return
        
        self.running = True
        
        def run_scheduler():
            logger.info("Scheduler started")
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        
        self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        logger.info("Scheduler thread started")
    
    def stop(self):
        """إيقاف الجدولة"""
        
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        
        logger.info("Scheduler stopped")
    
    def clear_all_jobs(self):
        """مسح جميع المهام المجدولة"""
        
        schedule.clear()
        self.jobs.clear()
        logger.info("All scheduled jobs cleared")
    
    def get_scheduled_jobs(self) -> Dict:
        """الحصول على قائمة بالمهام المجدولة"""
        
        jobs_info = {}
        for job in schedule.get_jobs():
            jobs_info[job.job_func.__name__] = {
                "next_run": job.next_run,
                "interval": str(job.interval),
                "unit": job.unit
            }
        
        return jobs_info
    
    def run_once_now(self, task_name: str):
        """تشغيل مهمة مرة واحدة الآن"""
        
        if task_name in self.jobs:
            job = self.jobs[task_name]
            job.run()
            return True
        
        logger.error(f"Task '{task_name}' not found")
        return False
    
    def update_schedule_time(self, task_name: str, new_time: str):
        """تحديث وقت الجدولة"""
        
        if task_name not in self.jobs:
            logger.error(f"Task '{task_name}' not found for update")
            return False
        
        try:
            # إلغاء المهمة القديمة
            schedule.cancel_job(self.jobs[task_name])
            
            # إنشاء مهمة جديدة
            task_func = self.jobs[task_name].job_func
            args = self.jobs[task_name].args
            kwargs = self.jobs[task_name].kwargs
            
            # إعادة الجدولة
            hour, minute = map(int, new_time.split(':'))
            job = schedule.every().day.at(new_time).do(
                self._run_task_with_logging, task_name, task_func, *args, **kwargs
            )
            
            self.jobs[task_name] = job
            logger.info(f"Updated schedule for task '{task_name}' to {new_time}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating schedule for task '{task_name}': {e}")
            return False


# وظائف مساعدة للجدولة
def calculate_next_schedule() -> Dict[str, datetime]:
    """حساب أوقات الجدولة التالية"""
    
    now = datetime.now()
    next_times = {}
    
    for i, schedule_time in enumerate(SCHEDULE_SETTINGS["shorts_schedule"]):
        task_name = f"short_{i+1}"
        hour, minute = map(int, schedule_time.split(':'))
        
        next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # إذا كان الوقت قد فات اليوم، جدوله للغد
        if next_run < now:
            next_run += timedelta(days=1)
        
        next_times[task_name] = next_run
    
    # وقت الفيديو التجميعي
    hour, minute = map(int, SCHEDULE_SETTINGS["compilation_schedule"].split(':'))
    next_compilation = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if next_compilation < now:
        next_compilation += timedelta(days=1)
    
    next_times["compilation"] = next_compilation
    
    return next_times


def is_time_for_task(schedule_time: str) -> bool:
    """التحقق إذا حان وقت المهمة"""
    
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    
    # السماح بفارق دقيقة واحدة
    scheduled_hour, scheduled_minute = map(int, schedule_time.split(':'))
    current_hour, current_minute = map(int, current_time.split(':'))
    
    return (current_hour == scheduled_hour and 
            abs(current_minute - scheduled_minute) <= 1)

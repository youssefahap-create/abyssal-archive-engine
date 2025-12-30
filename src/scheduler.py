"""
المجدول - تشغيل النظام تلقائياً
"""

import schedule
import time
from datetime import datetime
from threading import Thread
from pathlib import Path

from config.settings import *
from utils.logger import setup_logger

class TaskScheduler:
    def __init__(self):
        self.logger = setup_logger("scheduler", LOGS_DIR / "scheduler.log")
        self.is_running = False
        self.scheduled_jobs = []
        
    def setup_daily_schedule(self):
        """إعداد الجدولة اليومية"""
        # وقت التشغيل الرئيسي (بعد منتصف الليل)
        schedule.every().day.at("00:30").do(self._run_daily_tasks)
        
        # نسخة احتياطية إذا فشلت الأولى
        schedule.every().day.at("02:00").do(self._run_backup_tasks)
        
        self.logger.info("✅ تم إعداد الجدولة اليومية")
    
    def _run_daily_tasks(self):
        """تشغيل المهام اليومية"""
        if self.is_running:
            self.logger.warning("⚠️  النظام يعمل بالفعل، تخطي هذه الدورة")
            return
        
        self.is_running = True
        self.logger.info("⏰ بدء المهام اليومية المجدولة")
        
        try:
            from main import YouTubeShortsAutomation
            automation = YouTubeShortsAutomation()
            success = automation.run()
            
            if success:
                self.logger.info("✅ اكتملت المهام اليومية بنجاح")
            else:
                self.logger.error("❌ فشلت المهام اليومية")
                
        except Exception as e:
            self.logger.error(f"💥 خطأ في المهام اليومية: {e}", exc_info=True)
        
        finally:
            self.is_running = False
    
    def _run_backup_tasks(self):
        """تشغيل المهام الاحتياطية"""
        # التحقق إذا تم تنفيذ المهام بالفعل
        log_file = LOGS_DIR / "automation.log"
        today = datetime.now().strftime("%Y-%m-%d")
        
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if f"بدء التشغيل اليومي - {today}" in content:
                    self.logger.info("✅ تم تنفيذ المهام بالفعل، تخطي النسخة الاحتياطية")
                    return
        
        self.logger.info("🔄 تشغيل النسخة الاحتياطية")
        self._run_daily_tasks()
    
    def run_continuously(self):
        """تشغيل المجدول بشكل مستمر"""
        self.setup_daily_schedule()
        
        self.logger.info("🚀 بدء تشغيل المجدول...")
        
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # التحقق كل دقيقة
                
            except KeyboardInterrupt:
                self.logger.info("👋 إيقاف المجدول...")
                break
            except Exception as e:
                self.logger.error(f"⚠️  خطأ في المجدول: {e}")
                time.sleep(300)  # انتظار 5 دقائق عند الخطأ
    
    def update_schedule(self, uploaded_videos):
        """تحديث الجدولة بناءً على الفيديوهات المرفوعة"""
        schedule_file = LOGS_DIR / "upload_schedule.json"
        
        schedule_data = {
            "last_update": datetime.now().isoformat(),
            "total_uploads": len(uploaded_videos),
            "videos": uploaded_videos
        }
        
        with open(schedule_file, 'w', encoding='utf-8') as f:
            json.dump(schedule_data, f, indent=2)
        
        self.logger.info(f"📅 تم تحديث جدولة {len(uploaded_videos)} فيديو")

def start_scheduler():
    """بدء تشغيل المجدول في thread منفصل"""
    scheduler = TaskScheduler()
    thread = Thread(target=scheduler.run_continuously, daemon=True)
    thread.start()
    return scheduler

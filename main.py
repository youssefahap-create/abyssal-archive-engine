#!/usr/bin/env python3
"""
YouTube Shorts Automation System
نظام تشغيل تلقائي لقناة يوتيوب شورتس
"""

import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
import logging

# إضافة المسار للوحدات
sys.path.append(str(Path(__file__).parent))

from config.settings import *
from config.secrets_manager import SecretsManager
from src.content_generator import ContentGenerator
from src.media_processor import MediaProcessor
from src.video_creator import VideoCreator
from src.youtube_manager import YouTubeManager
from src.scheduler import TaskScheduler
from utils.logger import setup_logger

class YouTubeShortsAutomation:
    def __init__(self):
        """تهيئة النظام"""
        self.logger = setup_logger("automation", LOGS_DIR / "automation.log")
        self.secrets = SecretsManager()
        self.content_gen = ContentGenerator(self.secrets)
        self.media_proc = MediaProcessor(self.secrets)
        self.video_creator = VideoCreator()
        self.youtube = YouTubeManager(self.secrets)
        self.scheduler = TaskScheduler()
        
        self.today_shorts = []
        
    def generate_daily_content(self):
        """توليد محتوى اليوم"""
        self.logger.info("🎬 بدء توليد محتوى اليوم...")
        
        for i in range(CHANNEL_CONFIG["daily_shorts"]):
            short_num = i + 1
            self.logger.info(f"📝 توليد الشورت رقم {short_num}")
            
            try:
                # 1. توليد السؤال
                question_data = self.content_gen.generate_question()
                
                # 2. توليد الصوت
                audio_path = self.media_proc.generate_voiceover(question_data)
                
                # 3. معالجة الصور/الخلفيات
                background_path = self.media_proc.create_background(question_data)
                
                # 4. إنشاء الفيديو
                video_path = self.video_creator.create_short(
                    background=background_path,
                    audio=audio_path,
                    question_data=question_data,
                    short_number=short_num
                )
                
                # 5. إعداد الميتاداتا
                metadata = self.content_gen.generate_metadata(
                    question_data=question_data,
                    video_number=short_num
                )
                
                # 6. حفظ بيانات الشورت
                short_data = {
                    "video_path": video_path,
                    "metadata": metadata,
                    "question_data": question_data,
                    "upload_time": CHANNEL_CONFIG["optimal_times"][i]
                }
                
                self.today_shorts.append(short_data)
                self.logger.info(f"✅ تم إنشاء الشورت رقم {short_num}")
                
            except Exception as e:
                self.logger.error(f"❌ خطأ في إنشاء الشورت {short_num}: {e}")
                continue
        
        return len(self.today_shorts) > 0
    
    def create_compilation(self):
        """إنشاء فيديو تجميعي"""
        if len(self.today_shorts) < 2:
            self.logger.warning("لا يوجد شورتات كافية للتجميع")
            return None
        
        self.logger.info("🎞 إنشاء الفيديو التجميعي...")
        
        try:
            compilation_path = self.video_creator.create_compilation(
                shorts_data=self.today_shorts,
                day_date=datetime.now().strftime("%Y-%m-%d")
            )
            
            # إعداد ميتاداتا التجميع
            compilation_metadata = self.content_gen.generate_compilation_metadata(
                shorts_count=len(self.today_shorts),
                day_date=datetime.now().strftime("%B %d, %Y")
            )
            
            return {
                "video_path": compilation_path,
                "metadata": compilation_metadata,
                "upload_time": "22:00"  # وقت متأخر
            }
            
        except Exception as e:
            self.logger.error(f"❌ خطأ في إنشاء الفيديو التجميعي: {e}")
            return None
    
    def upload_content(self):
        """رفع المحتوى إلى يوتيوب"""
        self.logger.info("📤 بدء رفع المحتوى...")
        
        uploaded_shorts = []
        
        # رفع الشورتات الفردية
        for short in self.today_shorts:
            try:
                video_id = self.youtube.upload_video(
                    video_path=short["video_path"],
                    metadata=short["metadata"],
                    schedule_time=short["upload_time"]
                )
                
                if video_id:
                    uploaded_shorts.append({
                        "video_id": video_id,
                        "title": short["metadata"]["title"]
                    })
                    self.logger.info(f"✅ تم رفع: {short['metadata']['title']}")
                    
                    # تأخير بين الرفعات لتجنب rate limits
                    time.sleep(30)
                    
            except Exception as e:
                self.logger.error(f"❌ خطأ في رفع الفيديو: {e}")
                continue
        
        # رفع الفيديو التجميعي
        compilation = self.create_compilation()
        if compilation:
            try:
                comp_id = self.youtube.upload_video(
                    video_path=compilation["video_path"],
                    metadata=compilation["metadata"],
                    schedule_time=compilation["upload_time"],
                    is_compilation=True
                )
                
                if comp_id:
                    self.logger.info("✅ تم رفع الفيديو التجميعي")
                    
            except Exception as e:
                self.logger.error(f"❌ خطأ في رفع الفيديو التجميعي: {e}")
        
        return uploaded_shorts
    
    def cleanup(self):
        """تنظيف الملفات المؤقتة"""
        self.logger.info("🧹 تنظيف الملفات المؤقتة...")
        
        temp_files = list(TEMP_DIR.glob("*"))
        for file in temp_files:
            try:
                if file.is_file():
                    file.unlink()
            except Exception as e:
                self.logger.warning(f"⚠️  تعذر حذف {file}: {e}")
        
        # الاحتفاظ بملفات اليوم فقط في assets
        keep_pattern = datetime.now().strftime("%Y%m%d")
        old_assets = [f for f in ASSETS_DIR.glob("*") 
                     if f.is_file() and keep_pattern not in f.name]
        
        for asset in old_assets[:max(0, len(old_assets)-50)]:  # احتفظ بـ 50 ملف فقط
            try:
                asset.unlink()
            except:
                pass
    
    def run_daily_pipeline(self):
        """تشغيل خط العمل اليومي الكامل"""
        self.logger.info("="*50)
        self.logger.info(f"🚀 بدء التشغيل اليومي - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        self.logger.info("="*50)
        
        try:
            # 1. توليد المحتوى
            if not self.generate_daily_content():
                self.logger.error("❌ فشل في توليد المحتوى")
                return False
            
            # 2. رفع المحتوى
            uploaded = self.upload_content()
            
            # 3. التنظيف
            self.cleanup()
            
            # 4. تسجيل النتائج
            self.logger.info(f"📊 ملخص اليوم: تم رفع {len(uploaded)} من أصل {CHANNEL_CONFIG['daily_shorts']} شورت")
            
            if uploaded:
                # تحديث جدول الرفعات
                self.scheduler.update_schedule(uploaded)
                
                # حفظ سجل الرفع
                self._save_upload_log(uploaded)
            
            return len(uploaded) > 0
            
        except Exception as e:
            self.logger.error(f"💥 خطأ غير متوقع: {e}", exc_info=True)
            return False
    
    def _save_upload_log(self, uploaded_videos):
        """حفظ سجل الرفعات"""
        log_file = LOGS_DIR / "uploads_log.csv"
        
        header = "date,time,video_id,title,upload_status\n"
        if not log_file.exists():
            log_file.write_text(header)
        
        timestamp = datetime.now().strftime("%Y-%m-%d,%H:%M:%S")
        
        with open(log_file, 'a', encoding='utf-8') as f:
            for video in uploaded_videos:
                f.write(f"{timestamp},{video['video_id']},{video['title']},success\n")
    
    def run(self):
        """الدالة الرئيسية للتشغيل"""
        success = self.run_daily_pipeline()
        
        if success:
            self.logger.info("🎉 تم الانتهاء من العملية بنجاح!")
        else:
            self.logger.error("💔 فشل العملية")
        
        return success

def main():
    """الدالة الرئيسية"""
    automation = YouTubeShortsAutomation()
    
    # التحقق من وجود المفاتيح الأساسية
    if not automation.secrets.get_key("youtube", "api"):
        print("❌ يلزم وجود YouTube API Key")
        return False
    
    # التشغيل
    return automation.run()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

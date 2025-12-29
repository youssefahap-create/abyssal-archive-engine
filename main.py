import os
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# إضافة المسار للوحدات
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import (
    CONTENT_SETTINGS, SCHEDULE_SETTINGS, VIDEO_SETTINGS, YOUTUBE_SETTINGS
)
from config.secrets_manager import secrets_manager
from core.content_generator import ContentGenerator
from core.image_generator import ImageGenerator
from core.audio_generator import AudioGenerator
from core.video_editor import VideoEditor
from core.youtube_uploader import YouTubeUploader
from services.scheduler import Scheduler, calculate_next_schedule
from services.seo_optimizer import SEOOptimizer
from services.fallback_handler import FallbackHandler
from database.db_manager import db_manager
from utils.logger import logger, info, error, warning
from utils.helpers import generate_unique_id, ensure_directory


class YouTubeAutoChannel:
    """الفئة الرئيسية لإدارة قناة اليوتيوب التلقائية"""
    
    def __init__(self, test_mode: bool = False):
        """تهيئة النظام"""
        
        self.test_mode = test_mode
        self.content_gen = ContentGenerator()
        self.image_gen = ImageGenerator()
        self.audio_gen = AudioGenerator()
        self.video_editor = VideoEditor()
        self.youtube_uploader = YouTubeUploader()
        self.scheduler = Scheduler()
        self.seo_optimizer = SEOOptimizer()
        self.fallback_handler = FallbackHandler()
        
        self.today_shorts = []
        self.today_compilation = None
        
        info("YouTube Auto Channel initialized")
        
        if test_mode:
            warning("Running in TEST MODE - No videos will be uploaded to YouTube")
    
    def generate_daily_content(self):
        """توليد المحتوى اليومي"""
        
        info("Starting daily content generation")
        
        try:
            # توليد الأسئلة اليومية
            daily_questions = self.content_gen.generate_questions_for_day(
                count=CONTENT_SETTINGS["daily_shorts"]
            )
            
            info(f"Generated {len(daily_questions)} questions for today")
            
            self.today_shorts = []
            
            for i, question_data in enumerate(daily_questions, 1):
                info(f"Processing question {i}/{len(daily_questions)}: {question_data['question'][:50]}...")
                
                # إنشاء الفيديو
                video_path = self.video_editor.create_short_video(question_data)
                
                if video_path:
                    video_info = {
                        "question_data": question_data,
                        "video_path": video_path,
                        "short_number": i
                    }
                    self.today_shorts.append(video_info)
                    
                    info(f"Short video {i} created: {video_path}")
                else:
                    error(f"Failed to create short video for question {i}")
            
            info(f"Successfully created {len(self.today_shorts)} out of {len(daily_questions)} shorts")
            return len(self.today_shorts)
            
        except Exception as e:
            error(f"Error generating daily content: {e}")
            return 0
    
    def upload_daily_shorts(self):
        """رفع الشورتات اليومية"""
        
        if self.test_mode:
            info("TEST MODE: Skipping YouTube upload")
            return []
        
        if not self.today_shorts:
            warning("No shorts to upload today")
            return []
        
        info(f"Starting upload of {len(self.today_shorts)} shorts")
        
        uploaded_videos = []
        
        for i, short_info in enumerate(self.today_shorts, 1):
            try:
                question_data = short_info["question_data"]
                video_path = short_info["video_path"]
                
                # حساب وقت الجدولة
                schedule_idx = i - 1
                if schedule_idx < len(SCHEDULE_SETTINGS["shorts_schedule"]):
                    schedule_time_str = SCHEDULE_SETTINGS["shorts_schedule"][schedule_idx]
                    
                    # تحويل إلى كائن datetime
                    hour, minute = map(int, schedule_time_str.split(':'))
                    today = datetime.now().date()
                    schedule_time = datetime.combine(today, datetime.min.time()).replace(
                        hour=hour, minute=minute
                    )
                    
                    # إذا كان الوقت قد فات اليوم، نضيف يوم
                    if schedule_time < datetime.now():
                        schedule_time += timedelta(days=1)
                else:
                    schedule_time = None
                
                # تحسين بيانات التعريف
                metadata = self.seo_optimizer.optimize_metadata(question_data)
                
                info(f"Uploading short {i}/{len(self.today_shorts)} to YouTube...")
                
                # رفع الفيديو
                youtube_video_id = self.youtube_uploader.upload_short(
                    video_path=video_path,
                    question_data=question_data,
                    schedule_time=schedule_time
                )
                
                if youtube_video_id:
                    uploaded_videos.append({
                        "youtube_id": youtube_video_id,
                        "short_number": i,
                        "schedule_time": schedule_time,
                        "question": question_data["question"]
                    })
                    
                    info(f"Short {i} uploaded successfully: {youtube_video_id}")
                    
                    # حفظ في قاعدة البيانات
                    video_data = {
                        "video_id": youtube_video_id,
                        "question_id": question_data.get("question_id"),
                        "video_path": video_path,
                        "video_type": "short",
                        "title": metadata["title"],
                        "description": metadata["description"],
                        "tags": metadata["tags"],
                        "upload_status": "uploaded",
                        "scheduled_time": schedule_time.isoformat() if schedule_time else None
                    }
                    
                    db_manager.save_video(video_data)
                    
                else:
                    error(f"Failed to upload short {i}")
                    
            except Exception as e:
                error(f"Error uploading short {i}: {e}")
                # تسجيل الخطأ في قاعدة البيانات
                db_manager.log_error(
                    error_type="UploadError",
                    error_message=str(e),
                    module="main",
                    function="upload_daily_shorts"
                )
        
        info(f"Successfully uploaded {len(uploaded_videos)} out of {len(self.today_shorts)} shorts")
        return uploaded_videos
    
    def create_and_upload_compilation(self):
        """إنشاء ورفع الفيديو التجميعي"""
        
        if not self.today_shorts:
            warning("No shorts available for compilation")
            return None
        
        info("Creating compilation video...")
        
        try:
            # جمع مسارات الشورتات
            short_paths = [info["video_path"] for info in self.today_shorts]
            questions_data = [info["question_data"] for info in self.today_shorts]
            
            # إنشاء الفيديو التجميعي
            compilation_path = self.video_editor.create_compilation_video(short_paths)
            
            if not compilation_path:
                error("Failed to create compilation video")
                return None
            
            info(f"Compilation video created: {compilation_path}")
            
            if self.test_mode:
                info("TEST MODE: Skipping compilation upload")
                return compilation_path
            
            # حساب وقت الجدولة للتجميع
            hour, minute = map(int, SCHEDULE_SETTINGS["compilation_schedule"].split(':'))
            today = datetime.now().date()
            schedule_time = datetime.combine(today, datetime.min.time()).replace(
                hour=hour, minute=minute
            )
            
            if schedule_time < datetime.now():
                schedule_time += timedelta(days=1)
            
            # رفع الفيديو التجميعي
            youtube_video_id = self.youtube_uploader.upload_compilation(
                video_path=compilation_path,
                shorts_data=questions_data,
                schedule_time=schedule_time
            )
            
            if youtube_video_id:
                info(f"Compilation uploaded successfully: {youtube_video_id}")
                
                # حفظ في قاعدة البيانات
                video_data = {
                    "video_id": youtube_video_id,
                    "video_path": compilation_path,
                    "video_type": "compilation",
                    "title": f"Daily Compilation - {datetime.now().strftime('%B %d, %Y')}",
                    "upload_status": "uploaded",
                    "scheduled_time": schedule_time.isoformat()
                }
                
                db_manager.save_video(video_data)
                
                self.today_compilation = {
                    "youtube_id": youtube_video_id,
                    "video_path": compilation_path,
                    "schedule_time": schedule_time
                }
                
                return youtube_video_id
            else:
                error("Failed to upload compilation video")
                return None
                
        except Exception as e:
            error(f"Error creating/uploading compilation: {e}")
            db_manager.log_error(
                error_type="CompilationError",
                error_message=str(e),
                module="main",
                function="create_and_upload_compilation"
            )
            return None
    
    def run_daily_pipeline(self):
        """تشغيل خط العمل اليومي الكامل"""
        
        info("=" * 60)
        info("Starting Daily Pipeline")
        info("=" * 60)
        
        start_time = datetime.now()
        
        # الخطوة 1: توليد المحتوى
        info("[1/3] Generating daily content...")
        shorts_count = self.generate_daily_content()
        
        if shorts_count == 0:
            error("No content generated, stopping pipeline")
            return False
        
        # الخطوة 2: رفع الشورتات
        info("[2/3] Uploading daily shorts...")
        uploaded_shorts = self.upload_daily_shorts()
        
        # الخطوة 3: إنشاء ورفع التجميع
        info("[3/3] Creating and uploading compilation...")
        compilation_id = self.create_and_upload_compilation()
        
        # حساب وقت التنفيذ
        execution_time = datetime.now() - start_time
        
        # عرض التقرير النهائي
        info("=" * 60)
        info("Daily Pipeline Completed")
        info("=" * 60)
        info(f"Generated: {shorts_count} shorts")
        info(f"Uploaded: {len(uploaded_shorts)} shorts")
        info(f"Compilation: {'✓' if compilation_id else '✗'}")
        info(f"Total time: {execution_time.total_seconds():.2f} seconds")
        info("=" * 60)
        
        return len(uploaded_shorts) > 0
    
    def run_scheduled_task(self, task_type: str, task_number: int = None):
        """تشغيل مهمة مجدولة"""
        
        info(f"Running scheduled task: {task_type} {task_number if task_number else ''}")
        
        if task_type == "short" and task_number:
            # تشغيل مهمة شورت واحدة
            if task_number <= len(self.today_shorts):
                short_info = self.today_shorts[task_number - 1]
                
                if not self.test_mode:
                    # حساب وقت الجدولة
                    schedule_idx = task_number - 1
                    if schedule_idx < len(SCHEDULE_SETTINGS["shorts_schedule"]):
                        schedule_time_str = SCHEDULE_SETTINGS["shorts_schedule"][schedule_idx]
                        hour, minute = map(int, schedule_time_str.split(':'))
                        today = datetime.now().date()
                        schedule_time = datetime.combine(today, datetime.min.time()).replace(
                            hour=hour, minute=minute
                        )
                        
                        if schedule_time < datetime.now():
                            schedule_time += timedelta(days=1)
                    else:
                        schedule_time = None
                    
                    # رفع الفيديو
                    youtube_video_id = self.youtube_uploader.upload_short(
                        video_path=short_info["video_path"],
                        question_data=short_info["question_data"],
                        schedule_time=schedule_time
                    )
                    
                    if youtube_video_id:
                        info(f"Short {task_number} uploaded: {youtube_video_id}")
                    else:
                        error(f"Failed to upload short {task_number}")
                else:
                    info(f"TEST MODE: Would upload short {task_number}")
        
        elif task_type == "compilation":
            # تشغيل مهمة الفيديو التجميعي
            self.create_and_upload_compilation()
        
        else:
            warning(f"Unknown task type: {task_type}")
    
    def setup_scheduler(self):
        """إعداد الجدولة التلقائية"""
        
        info("Setting up automated scheduler...")
        
        # جدولة الشورتات اليومية
        self.scheduler.schedule_short_tasks(
            self.run_daily_pipeline
        )
        
        # جدولة الفيديو التجميعي
        self.scheduler.schedule_compilation_task(
            lambda: self.run_scheduled_task("compilation")
        )
        
        # عرض الجدولة
        next_schedule = calculate_next_schedule()
        info("Next scheduled times:")
        for task, time in next_schedule.items():
            info(f"  {task}: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def start_scheduler(self):
        """بدء تشغيل الجدولة"""
        
        info("Starting scheduler...")
        self.scheduler.start()
        
        try:
            # الحفاظ على البرنامج شغال
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            info("Shutting down scheduler...")
            self.scheduler.stop()
            info("Scheduler stopped")
    
    def test_system(self):
        """اختبار جميع مكونات النظام"""
        
        info("=" * 60)
        info("System Test Started")
        info("=" * 60)
        
        test_results = {
            "apis": {},
            "components": {},
            "overall": "PASS"
        }
        
        # اختبار واجهات برمجة التطبيقات
        info("Testing APIs...")
        api_status = secrets_manager.get_api_status()
        
        for api_name, has_keys in api_status.items():
            test_results["apis"][api_name] = "✓" if has_keys else "✗"
            if has_keys:
                info(f"  {api_name}: ✓")
            else:
                warning(f"  {api_name}: ✗ (No keys)")
        
        # اختبار توليد المحتوى
        info("Testing content generation...")
        try:
            question = self.content_gen.generate_question()
            if question:
                test_results["components"]["content_generation"] = "✓"
                info(f"  Content Generation: ✓ (Generated: {question['question'][:50]}...)")
            else:
                test_results["components"]["content_generation"] = "✗"
                error("  Content Generation: ✗")
        except Exception as e:
            test_results["components"]["content_generation"] = "✗"
            error(f"  Content Generation: ✗ ({e})")
        
        # اختبار توليد الصور
        info("Testing image generation...")
        try:
            test_prompt = "test image for system test"
            image = self.image_gen.generate_image_from_prompt(test_prompt)
            if image:
                test_results["components"]["image_generation"] = "✓"
                info(f"  Image Generation: ✓")
            else:
                test_results["components"]["image_generation"] = "✓ (Fallback)" 
                info(f"  Image Generation: ✓ (Using fallback)")
        except Exception as e:
            test_results["components"]["image_generation"] = "✗"
            error(f"  Image Generation: ✗ ({e})")
        
        # اختبار توليد الصوت
        info("Testing audio generation...")
        try:
            test_text = "This is a test audio for system testing."
            audio = self.audio_gen.generate_fallback_audio(test_text)
            if audio:
                test_results["components"]["audio_generation"] = "✓"
                info(f"  Audio Generation: ✓")
            else:
                test_results["components"]["audio_generation"] = "✗"
                error(f"  Audio Generation: ✗")
        except Exception as e:
            test_results["components"]["audio_generation"] = "✗"
            error(f"  Audio Generation: ✗ ({e})")
        
        # اختبار قاعدة البيانات
        info("Testing database...")
        try:
            db_manager.save_question({
                "question": "Test question for system test",
                "answer": "Test answer",
                "category": "test",
                "difficulty": "easy"
            })
            test_results["components"]["database"] = "✓"
            info(f"  Database: ✓")
        except Exception as e:
            test_results["components"]["database"] = "✗"
            error(f"  Database: ✗ ({e})")
        
        # تحديد النتيجة الإجمالية
        failed_components = [comp for comp, status in test_results["components"].items() if status == "✗"]
        if failed_components:
            test_results["overall"] = "FAIL"
            error(f"System test FAILED for components: {failed_components}")
        else:
            info("System test PASSED")
        
        info("=" * 60)
        info("System Test Completed")
        info("=" * 60)
        
        return test_results
    
    def show_system_status(self):
        """عرض حالة النظام"""
        
        info("=" * 60)
        info("System Status")
        info("=" * 60)
        
        # حالة واجهات برمجة التطبيقات
        api_status = secrets_manager.get_api_status()
        available_apis = [api for api, available in api_status.items() if available]
        info(f"Available APIs: {len(available_apis)}/{len(api_status)}")
        
        # إحصائيات قاعدة البيانات
        try:
            # عدد الأسئلة
            conn = db_manager._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM questions")
            total_questions = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM questions WHERE used = 0")
            unused_questions = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM videos")
            total_videos = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM videos WHERE upload_status = 'uploaded'")
            uploaded_videos = cursor.fetchone()[0]
            
            conn.close()
            
            info(f"Questions: {unused_questions}/{total_questions} unused")
            info(f"Videos: {uploaded_videos}/{total_videos} uploaded")
            
        except Exception as e:
            error(f"Error getting database stats: {e}")
        
        # حالة الملفات
        assets_dir = Path("assets")
        if assets_dir.exists():
            generated_dir = assets_dir / "generated"
            if generated_dir.exists():
                video_files = list(generated_dir.rglob("*.mp4"))
                info(f"Generated videos: {len(video_files)}")
        
        # الجدولة القادمة
        next_schedule = calculate_next_schedule()
        if next_schedule:
            info("Next scheduled tasks:")
            for task, time in next_schedule.items():
                time_str = time.strftime("%H:%M")
                info(f"  {task}: {time_str}")
        
        info("=" * 60)


def main():
    """الدالة الرئيسية"""
    
    parser = argparse.ArgumentParser(description="YouTube Auto Channel System")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    parser.add_argument("--run-once", action="store_true", help="Run daily pipeline once and exit")
    parser.add_argument("--schedule", action="store_true", help="Start the scheduler")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--test-all", action="store_true", help="Test all system components")
    parser.add_argument("--generate", type=int, help="Generate N test shorts")
    
    args = parser.parse_args()
    
    # إنشاء النظام
    system = YouTubeAutoChannel(test_mode=args.test)
    
    if args.status:
        system.show_system_status()
        return
    
    if args.test_all:
        system.test_system()
        return
    
    if args.generate:
        info(f"Generating {args.generate} test shorts...")
        for i in range(args.generate):
            question = system.content_gen.generate_question()
            if question:
                video_path = system.video_editor.create_short_video(question)
                if video_path:
                    info(f"Created test short {i+1}: {video_path}")
        return
    
    if args.run_once:
        success = system.run_daily_pipeline()
        sys.exit(0 if success else 1)
    
    if args.schedule:
        # إعداد وبدء الجدولة
        system.setup_scheduler()
        system.start_scheduler()
        return
    
    # الوضع الافتراضي: تشغيل خط العمل اليومي مرة واحدة
    info("No arguments provided, running daily pipeline once...")
    success = system.run_daily_pipeline()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        info("System stopped by user")
        sys.exit(0)
    except Exception as e:
        error(f"Fatal error: {e}")
        sys.exit(1)

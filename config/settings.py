"""
إعدادات المشروع الرئيسية
"""
import os
from pathlib import Path

# المسارات الأساسية
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
TEMPLATES_DIR = ASSETS_DIR / "templates"
BACKGROUNDS_DIR = ASSETS_DIR / "backgrounds"
LOCAL_IMAGES_DIR = ASSETS_DIR / "local_images"
LOCAL_AUDIO_DIR = ASSETS_DIR / "local_audio"
GENERATED_DIR = ASSETS_DIR / "generated"
UPLOADS_DIR = ASSETS_DIR / "uploads"

# إنشاء المجلدات إذا لم تكن موجودة
for directory in [ASSETS_DIR, TEMPLATES_DIR, BACKGROUNDS_DIR, LOCAL_IMAGES_DIR, 
                  LOCAL_AUDIO_DIR, GENERATED_DIR, UPLOADS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# إعدادات الفيديو
VIDEO_SETTINGS = {
    "resolution": (1080, 1920),  # شورت عمودي
    "duration": 18,  # مدة الفيديو بالثواني (15 ثانية سؤال + 3 ثانية إجابة)
    "fps": 30,
    "background_blur": 15,  # قوة البلور للخلفية
    "font_path": str(BASE_DIR / "assets" / "fonts" / "Arial.ttf"),
    "question_duration": 15,  # مدة السؤال
    "answer_duration": 3,  # مدة ظهور الإجابة
}

# إعدادات المحتوى
CONTENT_SETTINGS = {
    "daily_shorts": 4,
    "compilation_video": True,
    "target_language": "en",
    "content_types": ["general_knowledge", "flags", "landmarks", "animals", "riddles"],
    "min_questions_per_day": 10,  # أسئلة احتياطية
}

# إعدادات النشر
SCHEDULE_SETTINGS = {
    "timezone": "GMT",
    "shorts_schedule": ["08:00", "12:00", "16:00", "20:00"],
    "compilation_schedule": "22:00",
    "retry_attempts": 3,
    "retry_delay": 300,  # 5 دقائق
}

# إعدادات YouTube
YOUTUBE_SETTINGS = {
    "privacy_status": "public",
    "category_id": "22",  # People & Blogs
    "default_language": "en",
    "tags": ["quiz", "trivia", "brainteaser", "generalknowledge", "puzzle", "shortsviral"],
    "description_template": """🧠 Test your knowledge in 15 seconds!
    
Can you solve this? Write your answer in the comments! ⬇️

🔔 Subscribe for daily brain teasers: [CHANNEL_LINK]
📱 Follow us for more challenges!

#quiz #trivia #brainteaser #generalknowledge #puzzle #shorts #shortsviral"""
}

# إعدادات Fallback
FALLBACK_ORDER = {
    "audio": ["elevenlabs", "groq", "openai", "google", "pyttsx3"],
    "image_generation": ["getimg", "replicate", "openai", "search", "local"],
    "content_generation": ["gemini", "openai", "claude", "huggingface", "local_db"],
    "image_search": ["pexels", "pixabay", "unsplash", "local"],
}

# حدود API
API_LIMITS = {
    "max_requests_per_day": {
        "elevenlabs": 10000,
        "openai": 200,
        "gemini": 60,
        "getimg": 100,
        "replicate": 50,
    }
}

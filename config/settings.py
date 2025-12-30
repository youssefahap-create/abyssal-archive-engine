import os
from datetime import datetime
from pathlib import Path

# مسارات الملفات
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
TEMP_DIR = BASE_DIR / "temp"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# إنشاء المجلدات
for directory in [ASSETS_DIR, TEMP_DIR, OUTPUT_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# إعدادات القناة
CHANNEL_CONFIG = {
    "channel_id": os.getenv("YT_CHANNEL_ID"),
    "target_language": "en",
    "daily_shorts": 4,
    "optimal_times": ["08:00", "12:00", "16:00", "20:00"],  # UTC
    "short_duration": 18,  # ثانية
    "answer_display_time": 3,  # ثانية
    "countdown_duration": 15,  # ثانية
}

# إعدادات المحتوى
CONTENT_CONFIG = {
    "question_types": [
        "general_knowledge",
        "flag_identification",
        "landmark_recognition",
        "country_from_image",
        "scientific_facts",
        "historical_events"
    ],
    "difficulty_levels": ["easy", "medium", "hard"],
    "voice_phrases": [
        "If you know this quickly, you're in the top 95% of intelligent people!",
        "Think fast! Only geniuses get this in seconds.",
        "Can you beat the clock? Write your answer in comments!",
        "This separates average from extraordinary minds!"
    ]
}

# نظام Fallback لكل خدمة
FALLBACK_ORDER = {
    "tts": ["elevenlabs", "google_tts", "pyttsx3"],
    "image_gen": ["getimg", "replicate", "pexels", "pixabay", "unsplash"],
    "content_gen": ["gemini", "openai", "groq", "local_llm"],
    "video_gen": ["moviepy", "opencv"],
    "upload": ["youtube_api", "youtube_studio"]
}

# قوالب الميتاداتا
METADATA_TEMPLATES = {
    "title": "{question_type} Challenge #{number} | Can You Answer in {seconds}s?",
    "description": """🤔 Test your knowledge with this {difficulty} question!
⏱ Only {seconds} seconds to answer!
👇 Write your answer in the comments below!

{hashtags}

#Quiz #Challenge #TestYourBrain #ShortQuiz""",
    "tags": ["quiz", "challenge", "brain test", "knowledge", "trivia"],
    "hashtags": "#QuizTime #BrainTest #QuickChallenge #KnowledgeIsPower"
}

# إعدادات الجودة
QUALITY_SETTINGS = {
    "video_resolution": (1080, 1920),  # 9:16 للشورتس
    "fps": 30,
    "audio_bitrate": "192k",
    "video_bitrate": "10M"
}

# إعدادات الترند
TREND_SETTINGS = {
    "sources": ["reddit", "google_trends", "twitter"],
    "update_frequency": 6,  # ساعات
    "min_popularity": 1000
}

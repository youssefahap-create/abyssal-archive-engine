import os
from typing import Optional, Dict, Any
import pytz

class Config:
    """
    Configuration class for The Abyssal Archive YouTube Automation Project
    All sensitive data is loaded from environment variables
    """
    
    # API Keys - Loaded from environment variables
    CAMB_AI_KEY_1 = os.environ.get('CAMB_AI_KEY_1')
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
    COVERR_API_ID = os.environ.get('COVERR_API_ID')
    COVERR_API_KEY = os.environ.get('COVERR_API_KEY')
    ELEVEN_API_KEY_1 = os.environ.get('ELEVEN_API_KEY_1')
    ELEVEN_API_KEY_2 = os.environ.get('ELEVEN_API_KEY_2')
    ELEVEN_API_KEY_3 = os.environ.get('ELEVEN_API_KEY_3')
    FREEPIK_API_KEY = os.environ.get('FREEPIK_API_KEY')
    FREESOUND_API = os.environ.get('FREESOUND_API')
    FREESOUND_ID = os.environ.get('FREESOUND_ID')
    GEMINI_API_KEY_1 = os.environ.get('GEMINI_API_KEY_1')
    GEMINI_API_KEY_2 = os.environ.get('GEMINI_API_KEY_2')
    GETIMG_API_KEY_1 = os.environ.get('GETIMG_API_KEY_1')
    GETIMG_API_KEY_2 = os.environ.get('GETIMG_API_KEY_2')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    HF_API_TOKEN_1 = os.environ.get('HF_API_TOKEN_1')
    INTERNET_ARCHIVE_ACCESS_KEY = os.environ.get('INTERNET_ARCHIVE_ACCESS_KEY')
    INTERNET_ARCHIVE_SECRET_KEY = os.environ.get('INTERNET_ARCHIVE_SECRET_KEY')
    NASA_API_KEY = os.environ.get('NASA_API_KEY')
    NEWS_API = os.environ.get('NEWS_API')
    NOAA_API_KEY = os.environ.get('NOAA_API_KEY')
    OPENAI_API_KEY_1 = os.environ.get('OPENAI_API_KEY_1')
    OPENAI_API_KEY_2 = os.environ.get('OPENAI_API_KEY_2')
    OPENROUTER_KEY = os.environ.get('OPENROUTER_KEY')
    PEXELS_API_KEY = os.environ.get('PEXELS_API_KEY')
    PIXABAY_API_KEY = os.environ.get('PIXABAY_API_KEY')
    REMOVE_BG_API = os.environ.get('REMOVE_BG_API')
    REPLICATE_API_TOKEN_1 = os.environ.get('REPLICATE_API_TOKEN_1')
    REPLICATE_API_TOKEN_2 = os.environ.get('REPLICATE_API_TOKEN_2')
    TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY')
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
    UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_ACCESS_KEY')
    UNSPLASH_ID = os.environ.get('UNSPLASH_ID')
    UNSPLASH_SECRET_KEY = os.environ.get('UNSPLASH_SECRET_KEY')
    VECTEEZY_API_KEY = os.environ.get('VECTEEZY_API_KEY')
    VECTEEZY_ID_KEY = os.environ.get('VECTEEZY_ID_KEY')
    YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
    YT_CHANNEL_ID = os.environ.get('YT_CHANNEL_ID')
    YT_CLIENT_ID_1 = os.environ.get('YT_CLIENT_ID_1')
    YT_CLIENT_ID_2 = os.environ.get('YT_CLIENT_ID_2')
    YT_CLIENT_SECRET_1 = os.environ.get('YT_CLIENT_SECRET_1')
    YT_CLIENT_SECRET_2 = os.environ.get('YT_CLIENT_SECRET_2')
    YT_REFRESH_TOKEN_1 = os.environ.get('YT_REFRESH_TOKEN_1')
    YT_REFRESH_TOKEN_2 = os.environ.get('YT_REFRESH_TOKEN_2')

    # Project Configuration
    PROJECT_NAME = "The Abyssal Archive"
    CHANNEL_TAGLINE = "Uncovering the world's darkest mysteries and unexplained phenomena"
    
    # YouTube Upload Configuration
    MAX_UPLOADS_PER_DAY = 6  # 2 long videos + 4 shorts
    YOUTUBE_QUOTA_PER_UPLOAD = 1600  # Standard quota units per upload
    
    # Video Production Settings
    LONG_VIDEO_DURATION_MIN = 180  # 3 minutes minimum
    LONG_VIDEO_DURATION_MAX = 360  # 6 minutes maximum
    SHORT_VIDEO_DURATION = 60      # 1 minute for shorts
    
    # Content Categories
    CONTENT_CATEGORIES = {
        "space": "Cosmic mysteries and unexplained space phenomena",
        "ocean": "Deep ocean secrets and underwater anomalies", 
        "history": "Historical mysteries and unsolved cases",
        "crime": "True crime and unexplained disappearances",
        "paranormal": "Supernatural and paranormal investigations"
    }
    
    # Content Sources
    WIKIPEDIA_LISTS = [
        "List of unexplained disappearances",
        "List of unsolved mysteries", 
        "List of cryptids",
        "List of mysterious places",
        "List of historical mysteries"
    ]
    
    # Image Generation Prompts
    IMAGE_PROMPTS = {
        "fog": "misty foggy dark atmosphere",
        "glowing_eyes": "glowing red eyes in darkness",
        "vortex": "spinning vortex portal dark energy",
        "silhouette": "dark silhouette against fog",
        "abandoned": "abandoned building overgrown decayed"
    }
    
    # Thumbnail Design Elements
    THUMBNAIL_ELEMENTS = {
        "high_contrast": True,
        "red_arrow": True,
        "glowing_effect": True,
        "vintage_filter": True
    }
    
    # Audio Settings
    AUDIO_SETTINGS = {
        "voice_model": "en-US-ChristopherNeural",  # Microsoft Edge TTS
        "pitch_shift": -10,  # Lower pitch for deeper voice
        "speed_adjustment": -5,  # Slightly slower
        "audio_effects": ["8D", "reverb", "low_pass_filter"]
    }
    
    # Video Effects
    VIDEO_EFFECTS = {
        "ken_burns_zoom": True,
        "vhs_overlay": True,
        "text_overlays": True,
        "flash_warnings": True
    }
    
    # Publishing Schedule (New York Time)
    PUBLISHING_TIMES_NY = [
        "14:00",  # 2 PM EST
        "19:00"   # 7 PM EST
    ]
    
    # Timezone Settings
    NY_TZ = pytz.timezone('America/New_York')
    UTC_TZ = pytz.UTC
    
    # SEO and Metadata
    SEO_KEYWORDS = [
        "mystery", "scary facts", "unexplained", "paranormal", 
        "true crime", "cosmic horror", "deep ocean", "ancient mysteries",
        "unsolved", "cryptid", "haunted", "supernatural"
    ]
    
    # Telegram Bot Configuration
    TELEGRAM_ENABLED = bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)
    
    # Safety Filters
    AD_SAFE_FILTER_ENABLED = True
    CONTENT_MODERATION_ENABLED = True
    
    @classmethod
    def validate_secrets(cls) -> Dict[str, bool]:
        """Validate that critical secrets are available"""
        critical_secrets = [
            'YT_CHANNEL_ID', 'YT_CLIENT_ID_1', 'YT_CLIENT_SECRET_1', 
            'YT_REFRESH_TOKEN_1'
        ]
        
        validation_results = {}
        for secret_name in critical_secrets:
            secret_value = getattr(cls, secret_name)
            validation_results[secret_name] = bool(secret_value)
        
        return validation_results

# Initialize configuration
config = Config()

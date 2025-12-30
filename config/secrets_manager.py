import os
from typing import Dict, Optional

class SecretsManager:
    def __init__(self):
        self.secrets = {
            # TTS APIs
            "ELEVEN_API_KEY_1": os.getenv("ELEVEN_API_KEY_1"),
            "ELEVEN_API_KEY_2": os.getenv("ELEVEN_API_KEY_2"),
            "ELEVEN_API_KEY_3": os.getenv("ELEVEN_API_KEY_3"),
            "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
            
            # AI Content APIs
            "GEMINI_API_KEY_1": os.getenv("GEMINI_API_KEY_1"),
            "GEMINI_API_KEY_2": os.getenv("GEMINI_API_KEY_2"),
            "OPENAI_API_KEY_1": os.getenv("OPENAI_API_KEY_1"),
            "OPENAI_API_KEY_2": os.getenv("OPENAI_API_KEY_2"),
            
            # Image APIs
            "GETIMG_API_KEY_1": os.getenv("GETIMG_API_KEY_1"),
            "GETIMG_API_KEY_2": os.getenv("GETIMG_API_KEY_2"),
            "PEXELS_API_KEY": os.getenv("PEXELS_API_KEY"),
            "PIXABAY_API_KEY": os.getenv("PIXABAY_API_KEY"),
            "UNSPLASH_ACCESS_KEY": os.getenv("UNSPLASH_ACCESS_KEY"),
            
            # Video APIs
            "COVERR_API_KEY": os.getenv("COVERR_API_KEY"),
            
            # YouTube APIs
            "YOUTUBE_API_KEY": os.getenv("YOUTUBE_API_KEY"),
            "YT_REFRESH_TOKEN_1": os.getenv("YT_REFRESH_TOKEN_1"),
            "YT_REFRESH_TOKEN_2": os.getenv("YT_REFRESH_TOKEN_2"),
            
            # Misc APIs
            "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"),
            "REPLICATE_API_TOKEN_1": os.getenv("REPLICATE_API_TOKEN_1"),
            "REPLICATE_API_TOKEN_2": os.getenv("REPLICATE_API_TOKEN_2"),
            "NEWS_API": os.getenv("NEWS_API"),
            "CAMBAI_KEY": os.getenv("CAMBAI_KEY")
        }
        
        self.active_keys = {}
        self.failed_keys = set()
    
    def get_key(self, service: str, key_type: str) -> Optional[str]:
        """الحصول على مفتاح مع نظام fallback"""
        key_patterns = {
            "elevenlabs": ["ELEVEN_API_KEY_1", "ELEVEN_API_KEY_2", "ELEVEN_API_KEY_3"],
            "gemini": ["GEMINI_API_KEY_1", "GEMINI_API_KEY_2"],
            "openai": ["OPENAI_API_KEY_1", "OPENAI_API_KEY_2"],
            "getimg": ["GETIMG_API_KEY_1", "GETIMG_API_KEY_2"],
            "youtube": ["YOUTUBE_API_KEY"],
            "tts": ["ELEVEN_API_KEY_1", "GROQ_API_KEY"]
        }
        
        if service not in key_patterns:
            return None
            
        for key_name in key_patterns[service]:
            if key_name in self.failed_keys:
                continue
                
            key = self.secrets.get(key_name)
            if key and key.strip():
                self.active_keys[service] = key_name
                return key
        
        return None
    
    def mark_failed(self, key_name: str):
        """تحديد مفتاح فاشل"""
        self.failed_keys.add(key_name)
        # إزالة من المفاتيح النشطة
        for service, active_key in list(self.active_keys.items()):
            if active_key == key_name:
                del self.active_keys[service]
    
    def get_all_active(self) -> Dict:
        """الحصول على جميع المفاتيح النشطة"""
        return {service: self.secrets[key] 
                for service, key in self.active_keys.items()}

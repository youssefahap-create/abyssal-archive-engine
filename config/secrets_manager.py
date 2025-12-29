import os
import json
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class APIConfig:
    """تخزين إعدادات API"""
    name: str
    key_names: list
    current_key_index: int = 0
    keys: list = None
    
    def __post_init__(self):
        if self.keys is None:
            self.keys = []
            self.load_keys()
    
    def load_keys(self):
        """تحميل المفاتيح من متغيرات البيئة"""
        for key_name in self.key_names:
            key_value = os.getenv(key_name)
            if key_value:
                self.keys.append(key_value)
    
    def get_key(self):
        """الحصول على المفتاح التالي (Round Robin)"""
        if not self.keys:
            return None
        
        key = self.keys[self.current_key_index]
        self.current_key_index = (self.current_key_index + 1) % len(self.keys)
        return key
    
    def has_keys(self):
        """التحقق من وجود مفاتيح"""
        return len(self.keys) > 0

class SecretsManager:
    """مدير مركزي لجميع مفاتيح API"""
    
    def __init__(self):
        self.apis: Dict[str, APIConfig] = {}
        self._init_apis()
    
    def _init_apis(self):
        """تهيئة جميع واجهات برمجة التطبيقات"""
        
        # الصوتيات
        self.apis["elevenlabs"] = APIConfig(
            name="elevenlabs",
            key_names=["ELEVEN_API_KEY_1", "ELEVEN_API_KEY_2", "ELEVEN_API_KEY_3"]
        )
        
        self.apis["groq"] = APIConfig(
            name="groq",
            key_names=["GROQ_API_KEY"]
        )
        
        self.apis["openai"] = APIConfig(
            name="openai",
            key_names=["OPENAI_API_KEY_1", "OPENAI_API_KEY_2"]
        )
        
        self.apis["openrouter"] = APIConfig(
            name="openrouter",
            key_names=["OPENROUTER_KEY"]
        )
        
        # الصور
        self.apis["getimg"] = APIConfig(
            name="getimg",
            key_names=["GETIMG_API_KEY_1", "GETIMG_API_KEY_2"]
        )
        
        self.apis["replicate"] = APIConfig(
            name="replicate",
            key_names=["REPLICATE_API_TOKEN_1", "REPLICATE_API_TOKEN_2"]
        )
        
        self.apis["stable_diffusion"] = APIConfig(
            name="stable_diffusion",
            key_names=["HF_API_TOKEN_1"]
        )
        
        # توليد المحتوى
        self.apis["gemini"] = APIConfig(
            name="gemini",
            key_names=["GEMINI_API_KEY_1", "GEMINI_API_KEY_2"]
        )
        
        self.apis["claude"] = APIConfig(
            name="claude",
            key_names=["OPENROUTER_KEY"]  # يمكن استخدام OpenRouter للوصول إلى Claude
        )
        
        # البحث عن الصور
        self.apis["pexels"] = APIConfig(
            name="pexels",
            key_names=["PEXELS_API_KEY"]
        )
        
        self.apis["pixabay"] = APIConfig(
            name="pixabay",
            key_names=["PIXABAY_API_KEY"]
        )
        
        self.apis["unsplash"] = APIConfig(
            name="unsplash",
            key_names=["UNSPLASH_ACCESS_KEY", "UNSPLASH_SECRET_KEY"]
        )
        
        # خدمات أخرى
        self.apis["youtube"] = APIConfig(
            name="youtube",
            key_names=["YOUTUBE_API_KEY"]
        )
        
        self.apis["telegram"] = APIConfig(
            name="telegram",
            key_names=["TELEGRAM_BOT_TOKEN"]
        )
        
        self.apis["tavily"] = APIConfig(
            name="tavily",
            key_names=["TAVILY_API_KEY"]
        )
        
        self.apis["newsapi"] = APIConfig(
            name="newsapi",
            key_names=["NEWS_API"]
        )
        
        self.apis["nasa"] = APIConfig(
            name="nasa",
            key_names=["NASA_API_KEY"]
        )
        
        self.apis["noaa"] = APIConfig(
            name="noaa",
            key_names=["NOAA_API_KEY"]
        )
    
    def get_api_key(self, api_name: str) -> str:
        """الحصول على مفتاح API"""
        if api_name not in self.apis:
            return None
        
        api_config = self.apis[api_name]
        if not api_config.has_keys():
            return None
        
        return api_config.get_key()
    
    def get_all_keys(self, api_name: str) -> list:
        """الحصول على جميع مفاتيح API"""
        if api_name not in self.apis:
            return []
        
        return self.apis[api_name].keys
    
    def has_api(self, api_name: str) -> bool:
        """التحقق من توفر API"""
        if api_name not in self.apis:
            return False
        
        return self.apis[api_name].has_keys()
    
    def get_available_apis(self, category: str = None) -> list:
        """الحصول على واجهات برمجة التطبيقات المتاحة"""
        available = []
        for api_name, api_config in self.apis.items():
            if api_config.has_keys():
                available.append(api_name)
        
        if category:
            # يمكن تصفية حسب الفئة إذا لزم الأمر
            pass
        
        return available
    
    def get_api_status(self) -> Dict[str, bool]:
        """الحصول على حالة جميع واجهات برمجة التطبيقات"""
        status = {}
        for api_name, api_config in self.apis.items():
            status[api_name] = api_config.has_keys()
        
        return status

# إنشاء نسخة عامة
secrets_manager = SecretsManager()

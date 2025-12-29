import requests
import json
from typing import Optional, Dict, Any
from io import BytesIO

from config.settings import FALLBACK_ORDER
from config.secrets_manager import secrets_manager
from utils.logger import logger


class FallbackHandler:
    """معالج نظام Fallback للخدمات المختلفة"""
    
    def __init__(self):
        self.api_usage = {}  # تتبع استخدام API
    
    def generate_content(self, prompt: str, max_tokens: int = 150) -> Optional[str]:
        """توليد محتوى نصي باستخدام نظام Fallback"""
        
        apis_to_try = FALLBACK_ORDER["content_generation"]
        
        for api_name in apis_to_try:
            try:
                if api_name == "gemini" and secrets_manager.has_api("gemini"):
                    return self._generate_with_gemini(prompt, max_tokens)
                
                elif api_name == "openai" and secrets_manager.has_api("openai"):
                    return self._generate_with_openai(prompt, max_tokens)
                
                elif api_name == "claude" and secrets_manager.has_api("openrouter"):
                    return self._generate_with_claude(prompt, max_tokens)
                
                elif api_name == "huggingface" and secrets_manager.has_api("stable_diffusion"):
                    return self._generate_with_huggingface(prompt, max_tokens)
                
                elif api_name == "local_db":
                    # هنا يمكن استخدام قاعدة بيانات محلية
                    return None
                    
            except Exception as e:
                logger.warning(f"API {api_name} failed: {e}")
                continue
        
        logger.error("All content generation APIs failed")
        return None
    
    def generate_image(self, prompt: str) -> Optional[bytes]:
        """توليد صورة باستخدام نظام Fallback"""
        
        apis_to_try = FALLBACK_ORDER["image_generation"]
        
        for api_name in apis_to_try:
            try:
                if api_name == "getimg" and secrets_manager.has_api("getimg"):
                    return self._generate_with_getimg(prompt)
                
                elif api_name == "replicate" and secrets_manager.has_api("replicate"):
                    return self._generate_with_replicate(prompt)
                
                elif api_name == "openai" and secrets_manager.has_api("openai"):
                    return self._generate_with_dalle(prompt)
                
                elif api_name == "search":
                    # البحث عن صورة بدلاً من توليدها
                    return self.search_image(prompt)
                
                elif api_name == "local":
                    # استخدام صور محلية
                    return None
                    
            except Exception as e:
                logger.warning(f"Image API {api_name} failed: {e}")
                continue
        
        logger.error("All image generation APIs failed")
        return None
    
    def search_image(self, query: str) -> Optional[bytes]:
        """البحث عن صورة باستخدام نظام Fallback"""
        
        apis_to_try = FALLBACK_ORDER["image_search"]
        
        for api_name in apis_to_try:
            try:
                if api_name == "pexels" and secrets_manager.has_api("pexels"):
                    return self._search_with_pexels(query)
                
                elif api_name == "pixabay" and secrets_manager.has_api("pixabay"):
                    return self._search_with_pixabay(query)
                
                elif api_name == "unsplash" and secrets_manager.has_api("unsplash"):
                    return self._search_with_unsplash(query)
                
                elif api_name == "local":
                    # استخدام صور محلية
                    return None
                    
            except Exception as e:
                logger.warning(f"Image search API {api_name} failed: {e}")
                continue
        
        logger.error("All image search APIs failed")
        return None
    
    def generate_speech(self, text: str) -> Optional[bytes]:
        """توليد كلام باستخدام نظام Fallback"""
        
        apis_to_try = FALLBACK_ORDER["audio"]
        
        for api_name in apis_to_try:
            try:
                if api_name == "elevenlabs" and secrets_manager.has_api("elevenlabs"):
                    return self._generate_with_elevenlabs(text)
                
                elif api_name == "groq" and secrets_manager.has_api("groq"):
                    return self._generate_with_groq_tts(text)
                
                elif api_name == "openai" and secrets_manager.has_api("openai"):
                    return self._generate_with_openai_tts(text)
                
                elif api_name == "google":
                    return self._generate_with_google_tts(text)
                
                elif api_name == "pyttsx3":
                    return self._generate_with_pyttsx3(text)
                    
            except Exception as e:
                logger.warning(f"Speech API {api_name} failed: {e}")
                continue
        
        logger.error("All speech generation APIs failed")
        return None
    
    # ===== تطبيقات API المحددة =====
    
    def _generate_with_gemini(self, prompt: str, max_tokens: int) -> Optional[str]:
        """توليد محتوى باستخدام Gemini"""
        try:
            import google.generativeai as genai
            
            api_key = secrets_manager.get_api_key("gemini")
            if not api_key:
                return None
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return None
    
    def _generate_with_openai(self, prompt: str, max_tokens: int) -> Optional[str]:
        """توليد محتوى باستخدام OpenAI"""
        try:
            from openai import OpenAI
            
            api_key = secrets_manager.get_api_key("openai")
            if not api_key:
                return None
            
            client = OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return None
    
    def _generate_with_getimg(self, prompt: str) -> Optional[bytes]:
        """توليد صورة باستخدام GetIMG"""
        try:
            api_key = secrets_manager.get_api_key("getimg")
            if not api_key:
                return None
            
            url = "https://api.getimg.ai/v1/stable-diffusion/text-to-image"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "prompt": prompt,
                "width": 1080,
                "height": 1920,
                "steps": 25,
                "guidance": 7.5
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                # GetIMG قد ترجع URL أو بيانات مباشرة
                result = response.json()
                if "image" in result:
                    # إذا كانت الصورة مشفرة بـ base64
                    import base64
                    image_data = base64.b64decode(result["image"])
                    return image_data
                elif "url" in result:
                    # إذا كان هناك رابط للصورة
                    image_response = requests.get(result["url"])
                    return image_response.content
            
            return None
            
        except Exception as e:
            logger.error(f"GetIMG error: {e}")
            return None
    
    def _search_with_pexels(self, query: str) -> Optional[bytes]:
        """البحث عن صورة في Pexels"""
        try:
            api_key = secrets_manager.get_api_key("pexels")
            if not api_key:
                return None
            
            url = f"https://api.pexels.com/v1/search"
            
            headers = {
                "Authorization": api_key
            }
            
            params = {
                "query": query,
                "per_page": 1,
                "orientation": "portrait",
                "size": "large"
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("photos"):
                    photo_url = data["photos"][0]["src"]["original"]
                    image_response = requests.get(photo_url, timeout=10)
                    return image_response.content
            
            return None
            
        except Exception as e:
            logger.error(f"Pexels error: {e}")
            return None
    
    def _generate_with_elevenlabs(self, text: str) -> Optional[bytes]:
        """توليد كلام باستخدام ElevenLabs"""
        try:
            api_key = secrets_manager.get_api_key("elevenlabs")
            if not api_key:
                return None
            
            # استخدام Voice ID افتراضي
            voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                return response.content
            
            return None
            
        except Exception as e:
            logger.error(f"ElevenLabs error: {e}")
            return None
    
    def _generate_with_google_tts(self, text: str) -> Optional[bytes]:
        """توليد كلام باستخدام Google TTS"""
        try:
            from gtts import gTTS
            import tempfile
            
            tts = gTTS(text=text, lang='en', slow=False)
            
            # حفظ في ملف مؤقت
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
                temp_file = f.name
            
            tts.save(temp_file)
            
            # قراءة الملف كـ bytes
            with open(temp_file, 'rb') as f:
                audio_data = f.read()
            
            # حذف الملف المؤقت
            import os
            os.unlink(temp_file)
            
            return audio_data
            
        except Exception as e:
            logger.error(f"Google TTS error: {e}")
            return None
    
    def _generate_with_pyttsx3(self, text: str) -> Optional[bytes]:
        """توليد كلام باستخدام pyttsx3"""
        try:
            import pyttsx3
            import tempfile
            
            engine = pyttsx3.init()
            
            # إعدادات الصوت
            engine.setProperty('rate', 180)
            engine.setProperty('volume', 0.9)
            
            # حفظ في ملف مؤقت
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
                temp_file = f.name
            
            engine.save_to_file(text, temp_file)
            engine.runAndWait()
            
            # قراءة الملف كـ bytes
            with open(temp_file, 'rb') as f:
                audio_data = f.read()
            
            # حذف الملف المؤقت
            import os
            os.unlink(temp_file)
            
            return audio_data
            
        except Exception as e:
            logger.error(f"pyttsx3 error: {e}")
            return None
    
    # ===== تطبيقات API أخرى (مبسطة) =====
    
    def _generate_with_replicate(self, prompt: str) -> Optional[bytes]:
        """توليد صورة باستخدام Replicate"""
        # تنفيذ مماثل لـ GetIMG
        return None
    
    def _generate_with_dalle(self, prompt: str) -> Optional[bytes]:
        """توليد صورة باستخدام DALL-E"""
        # تنفيذ مماثل لـ GetIMG
        return None
    
    def _generate_with_claude(self, prompt: str, max_tokens: int) -> Optional[str]:
        """توليد محتوى باستخدام Claude عبر OpenRouter"""
        # تنفيذ مماثل لـ OpenAI
        return None
    
    def _generate_with_huggingface(self, prompt: str, max_tokens: int) -> Optional[str]:
        """توليد محتوى باستخدام HuggingFace"""
        # تنفيذ باستخدام نماذج HF
        return None
    
    def _search_with_pixabay(self, query: str) -> Optional[bytes]:
        """البحث عن صورة في Pixabay"""
        # تنفيذ مماثل لـ Pexels
        return None
    
    def _search_with_unsplash(self, query: str) -> Optional[bytes]:
        """البحث عن صورة في Unsplash"""
        # تنفيذ مماثل لـ Pexels
        return None
    
    def _generate_with_groq_tts(self, text: str) -> Optional[bytes]:
        """توليد كلام باستخدام Groq"""
        # تنفيذ مماثل لـ ElevenLabs
        return None
    
    def _generate_with_openai_tts(self, text: str) -> Optional[bytes]:
        """توليد كلام باستخدام OpenAI TTS"""
        # تنفيذ مماثل لـ ElevenLabs
        return None

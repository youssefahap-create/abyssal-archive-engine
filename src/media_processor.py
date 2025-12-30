import os
import tempfile
from pathlib import Path
from typing import Optional
import requests
from io import BytesIO

from config.settings import *
from config.secrets_manager import SecretsManager

class MediaProcessor:
    def __init__(self, secrets_manager: SecretsManager):
        self.secrets = secrets_manager
        self.tts_engine = None
        self.current_fallback = {
            "tts": 0,
            "image": 0,
            "voice": 0
        }
    
    def generate_voiceover(self, question_data: Dict) -> Path:
        """توليد صوت للسؤال مع نظام Fallback"""
        question_text = question_data["question"]
        
        # نص إضافي بعد السؤال
        additional_text = random.choice(CONTENT_CONFIG["voice_phrases"])
        full_text = f"{question_text}. {additional_text}"
        
        audio_path = TEMP_DIR / f"voice_{int(time.time())}.mp3"
        
        # المحاولة مع خدمات TTS بالترتيب
        tss_services = FALLBACK_ORDER["tts"]
        
        for service in tss_services[self.current_fallback["tts"]:]:
            try:
                if service == "elevenlabs":
                    audio = self._elevenlabs_tts(full_text)
                elif service == "google_tts":
                    audio = self._google_tts(full_text)
                elif service == "pyttsx3":
                    audio = self._pyttsx3_tts(full_text)
                else:
                    continue
                
                if audio:
                    with open(audio_path, 'wb') as f:
                        f.write(audio)
                    return audio_path
                    
            except Exception as e:
                print(f"⚠️  فشل {service}: {e}")
                self.current_fallback["tts"] += 1
                continue
        
        # إذا فشلت جميع الخدمات، استخدم ملف صوتي افتراضي
        return self._get_default_audio()
    
    def _elevenlabs_tts(self, text: str) -> Optional[bytes]:
        """استخدام ElevenLabs"""
        api_key = self.secrets.get_key("elevenlabs", "api")
        if not api_key:
            return None
        
        url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
        
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return response.content
        
        raise Exception(f"ElevenLabs API error: {response.status_code}")
    
    def _google_tts(self, text: str) -> Optional[bytes]:
        """استخدام Google TTS مجاناً"""
        try:
            from gtts import gTTS
            
            tts = gTTS(text=text, lang='en', slow=False)
            
            with BytesIO() as audio_bytes:
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                return audio_bytes.read()
                
        except Exception as e:
            print(f"⚠️  Google TTS error: {e}")
            return None
    
    def _pyttsx3_tts(self, text: str) -> Optional[bytes]:
        """استخدام pyttsx3 (محلي، لا يحتاج إنترنت)"""
        try:
            import pyttsx3
            import wave
            
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
            
            # حفظ في ملف مؤقت
            temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            temp_path = temp_file.name
            temp_file.close()
            
            engine.save_to_file(text, temp_path)
            engine.runAndWait()
            
            with open(temp_path, 'rb') as f:
                audio_data = f.read()
            
            # تحويل إلى MP3
            from pydub import AudioSegment
            audio = AudioSegment.from_wav(temp_path)
            mp3_data = BytesIO()
            audio.export(mp3_data, format="mp3")
            
            os.unlink(temp_path)
            return mp3_data.getvalue()
            
        except Exception as e:
            print(f"⚠️  pyttsx3 error: {e}")
            return None
    
    def _get_default_audio(self) -> Path:
        """الحصول على ملف صوتي افتراضي"""
        default_path = ASSETS_DIR / "default_voice.mp3"
        
        if not default_path.exists():
            # إنشاء ملف صوتي افتراضي
            self._create_default_audio(default_path)
        
        return default_path
    
    def create_background(self, question_data: Dict) -> Path:
        """إنشاء خلفية للفيديو"""
        image_path = TEMP_DIR / f"bg_{int(time.time())}.jpg"
        
        # المحاولة مع خدمات الصور بالترتيب
        image_services = FALLBACK_ORDER["image_gen"]
        
        for service in image_services[self.current_fallback["image"]:]:
            try:
                if service == "getimg":
                    image = self._getimg_generate(question_data["image_description"])
                elif service == "pexels":
                    image = self._pexels_search(question_data["image_description"])
                elif service == "pixabay":
                    image = self._pixabay_search(question_data["image_description"])
                elif service == "unsplash":
                    image = self._unsplash_search(question_data["image_description"])
                elif service == "replicate":
                    image = self._replicate_generate(question_data["image_description"])
                else:
                    continue
                
                if image:
                    # تطبيق تأثير blur
                    blurred = self._apply_blur(image)
                    blurred.save(image_path)
                    return image_path
                    
            except Exception as e:
                print(f"⚠️  فشل {service}: {e}")
                self.current_fallback["image"] += 1
                continue
        
        # إذا فشلت جميع الخدمات، استخدم خلفية افتراضية
        return self._get_default_background(question_data)
    
    def _apply_blur(self, image) -> Image:
        """تطبيق تأثير blur على الصورة"""
        from PIL import ImageFilter
        
        return image.filter(ImageFilter.GaussianBlur(radius=15))
    
    def _get_default_background(self, question_data: Dict) -> Path:
        """إنشاء خلفية افتراضية"""
        from PIL import Image, ImageDraw
        
        # ألوان متدرجة
        colors = [
            ("#1a2980", "#26d0ce"),  # أزرق
            ("#ff5e62", "#ff9966"),  # أحمر/برتقالي
            ("#614385", "#516395"),  # بنفسجي
            ("#11998e", "#38ef7d")   # أخضر
        ]
        
        color1, color2 = random.choice(colors)
        
        # إنشاء صورة متدرجة
        img = Image.new('RGB', QUALITY_SETTINGS["video_resolution"], color1)
        draw = ImageDraw.Draw(img)
        
        # إضافة بعض العناصر البسيطة
        for _ in range(50):
            x = random.randint(0, img.width)
            y = random.randint(0, img.height)
            r = random.randint(5, 20)
            opacity = random.randint(30, 100)
            draw.ellipse([x-r, y-r, x+r, y+r], 
                        fill=(255, 255, 255, opacity))
        
        # حفظ الصورة
        bg_path = TEMP_DIR / f"default_bg_{int(time.time())}.jpg"
        img.save(bg_path)
        
        return bg_path

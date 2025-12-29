import os
import io
import random
from typing import Optional, Tuple
import pyttsx3
from gtts import gTTS

from config.settings import GENERATED_DIR, VIDEO_SETTINGS
from config.secrets_manager import secrets_manager
from utils.logger import logger
from services.fallback_handler import FallbackHandler


class AudioGenerator:
    """فئة توليد الصوت"""
    
    def __init__(self):
        self.fallback_handler = FallbackHandler()
        self.generated_audio_dir = GENERATED_DIR / "audio"
        self.generated_audio_dir.mkdir(parents=True, exist_ok=True)
        
        # تحميل أصوات محلية إذا وجدت
        self.local_sounds = self._load_local_sounds()
    
    def _load_local_sounds(self) -> dict:
        """تحميل الأصوات المحلية"""
        sounds_dir = "assets/local_audio"
        sounds = {}
        
        if os.path.exists(sounds_dir):
            for file in os.listdir(sounds_dir):
                if file.endswith(('.mp3', '.wav', '.ogg')):
                    sound_name = os.path.splitext(file)[0]
                    sounds[sound_name] = os.path.join(sounds_dir, file)
        
        return sounds
    
    def generate_audio_for_question(self, question_data: dict) -> Optional[str]:
        """توليد صوت للسؤال"""
        
        question = question_data["question"]
        answer = question_data["answer"]
        category = question_data.get("category", "general")
        
        # إنشاء النص الصوتي
        speech_text = self._create_speech_text(question, answer, category)
        
        # توليد الصوت باستخدام نظام Fallback
        audio_bytes = self.fallback_handler.generate_speech(speech_text)
        
        if audio_bytes:
            # حفظ الصوت
            audio_id = f"question_{int(random.random() * 1000000)}"
            audio_path = self.generated_audio_dir / f"{audio_id}.mp3"
            
            with open(audio_path, 'wb') as f:
                f.write(audio_bytes)
            
            logger.info(f"Audio generated and saved: {audio_path}")
            return str(audio_path)
        
        return None
    
    def _create_speech_text(self, question: str, answer: str, category: str) -> str:
        """إنشاء نص كامل للتعليق الصوتي"""
        
        # نهاية السؤال (بدون علامة استفهام إذا كانت موجودة)
        clean_question = question.rstrip('?')
        
        # بدائل للعبارات التحفيزية
        prompts = [
            f"{clean_question}? If you know the answer in 15 seconds, you're in the top 5% of intelligent people. Write your answer in the comments!",
            f"Quick question: {clean_question}? Can you solve this in 15 seconds? Only 3% of people get this right. Let me know in the comments!",
            f"Brain teaser time! {clean_question}? You have 15 seconds. If you get it right, you're smarter than 95% of viewers. Comment your answer!",
            f"Test your knowledge! {clean_question}? You've got 15 seconds. Think you know it? Write it in the comments below!",
            f"Puzzle time! {clean_question}? Solve it in 15 seconds to prove your intelligence. Don't forget to comment your answer!"
        ]
        
        # اختيار عشوائي
        selected_prompt = random.choice(prompts)
        
        # إضافة تحسينات حسب الفئة
        if category == "flags":
            selected_prompt = f"Flag identification challenge! {clean_question}? You have 15 seconds. Which country's flag is this? Write your answer in the comments!"
        elif category == "landmarks":
            selected_prompt = f"Geography quiz! {clean_question}? Identify this landmark in 15 seconds. Comment the country or name below!"
        elif category == "animals":
            selected_prompt = f"Animal trivia! {clean_question}? You have 15 seconds to answer. What animal is this? Let us know in the comments!"
        elif category == "riddles":
            selected_prompt = f"Riddle time! {clean_question}? Solve this riddle in 15 seconds. Write your solution in the comments!"
        
        return selected_prompt
    
    def generate_countdown_beep(self, duration: int = 15) -> Optional[str]:
        """توليد صوت تنبيه للعداد"""
        
        # استخدام أصوات محلية إذا وجدت
        if "countdown_beep" in self.local_sounds:
            return self.local_sounds["countdown_beep"]
        
        # إذا لم توجد أصوات محلية، إنشاء صوت تنبيه بسيط باستخدام TTS
        try:
            # يمكن إنشاء صوت تنبيه باستخدام مكتبة بسيطة
            # في هذه الحالة، سنستخدم صوت تنبيه افتراضي
            # أو يمكن إنشاء ملف صوتي بسيط
            beep_path = self.generated_audio_dir / "countdown_beep.mp3"
            
            # إذا كان الملف موجودًا بالفعل
            if beep_path.exists():
                return str(beep_path)
            
            # محاولة إنشاء صوت تنبيه باستخدام gTTS
            tts = gTTS(text=".", lang='en')
            tts.save(str(beep_path))
            
            return str(beep_path)
            
        except Exception as e:
            logger.error(f"Error generating countdown beep: {e}")
            return None
    
    def get_background_music(self) -> Optional[str]:
        """الحصول على موسيقى خلفية"""
        
        # استخدام موسيقى محلية إذا وجدت
        if "background_music" in self.local_sounds:
            return self.local_sounds["background_music"]
        
        # يمكن إضافة موسيقى خلفية بسيطة هنا
        # أو استخدام مكتبات توليد موسيقى
        return None
    
    def merge_audio_files(self, speech_path: str, countdown_path: str = None, 
                        background_path: str = None) -> Optional[str]:
        """دمج ملفات الصوت"""
        
        try:
            from pydub import AudioSegment
            
            # تحميل الصوت الرئيسي
            speech_audio = AudioSegment.from_file(speech_path)
            
            # إذا كان هناك موسيقى خلفية
            if background_path and os.path.exists(background_path):
                bg_audio = AudioSegment.from_file(background_path)
                
                # تقليل مستوى الموسيقى الخلفية
                bg_audio = bg_audio - 20  # تقليل بمقدار 20 ديسيبل
                
                # جعل الموسيقى بنفس طول الصوت أو أقصر
                if len(bg_audio) < len(speech_audio):
                    # تكرار الموسيقى إذا كانت أقصر
                    bg_audio = bg_audio * (len(speech_audio) // len(bg_audio) + 1)
                    bg_audio = bg_audio[:len(speech_audio)]
                
                # دمج الصوت مع الموسيقى
                merged_audio = speech_audio.overlay(bg_audio)
            else:
                merged_audio = speech_audio
            
            # إضافة صوت التنبيه للعداد إذا كان موجودًا
            if countdown_path and os.path.exists(countdown_path):
                countdown_audio = AudioSegment.from_file(countdown_path)
                
                # يمكن إضافة صوت التنبيه في نهاية الصوت
                # أو في خلفية العداد المرئي
                pass
            
            # حفظ الصوت المدمج
            output_path = self.generated_audio_dir / f"merged_{int(random.random() * 1000000)}.mp3"
            merged_audio.export(str(output_path), format="mp3")
            
            logger.info(f"Audio merged and saved: {output_path}")
            return str(output_path)
            
        except ImportError:
            logger.warning("pydub not installed, using speech audio only")
            return speech_path
        except Exception as e:
            logger.error(f"Error merging audio: {e}")
            return speech_path
    
    def generate_fallback_audio(self, text: str) -> Optional[str]:
        """توليد صوت باستخدام أنظمة Fallback المحلية"""
        
        try:
            # المحاولة الأولى: استخدام gTTS (مجاني)
            audio_id = f"fallback_{int(random.random() * 1000000)}"
            audio_path = self.generated_audio_dir / f"{audio_id}.mp3"
            
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(str(audio_path))
            
            if os.path.getsize(audio_path) > 1000:  # التأكد من أن الملف غير فارغ
                return str(audio_path)
            
        except Exception as e:
            logger.error(f"gTTS failed: {e}")
        
        try:
            # المحاولة الثانية: استخدام pyttsx3 (محلي)
            engine = pyttsx3.init()
            
            # إعدادات الصوت
            engine.setProperty('rate', 180)  # سرعة الكلام
            engine.setProperty('volume', 0.9)  # مستوى الصوت
            
            # حفظ الصوت في ملف
            audio_id = f"fallback_pyttsx3_{int(random.random() * 1000000)}"
            audio_path = self.generated_audio_dir / f"{audio_id}.mp3"
            
            engine.save_to_file(text, str(audio_path))
            engine.runAndWait()
            
            if os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000:
                return str(audio_path)
            
        except Exception as e:
            logger.error(f"pyttsx3 failed: {e}")
        
        return None

import os
import random
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from moviepy.editor import VideoClip, ImageClip, AudioFileClip, CompositeVideoClip, TextClip
from moviepy.video.fx.all import resize

from config.settings import VIDEO_SETTINGS, GENERATED_DIR
from utils.logger import logger
from core.image_generator import ImageGenerator
from core.audio_generator import AudioGenerator


class VideoEditor:
    """فئة إنشاء وتحرير الفيديو"""
    
    def __init__(self):
        self.image_gen = ImageGenerator()
        self.audio_gen = AudioGenerator()
        self.generated_videos_dir = GENERATED_DIR / "videos"
        self.generated_shorts_dir = GENERATED_DIR / "shorts"
        
        # إنشاء المجلدات
        self.generated_videos_dir.mkdir(exist_ok=True)
        self.generated_shorts_dir.mkdir(exist_ok=True)
    
    def create_short_video(self, question_data: dict) -> Optional[str]:
        """إنشاء فيديو شورت كامل"""
        
        question = question_data["question"]
        answer = question_data["answer"]
        category = question_data.get("category", "general")
        
        logger.info(f"Creating short video for question: {question[:50]}...")
        
        # 1. توليد الصوت
        audio_path = self.audio_gen.generate_audio_for_question(question_data)
        if not audio_path:
            logger.error("Failed to generate audio")
            return None
        
        # 2. الحصول على الصورة
        background_image, image_source = self.image_gen.get_image_for_question(question_data)
        
        # 3. إنشاء الفيديو
        video_path = self._create_video_with_countdown(
            background_image=background_image,
            question=question,
            answer=answer,
            audio_path=audio_path,
            question_data=question_data
        )
        
        if video_path:
            logger.info(f"Short video created successfully: {video_path}")
            
            # حفظ معلومات الفيديو
            self._save_video_info(video_path, question_data, image_source)
            
            return video_path
        
        return None
    
    def _create_video_with_countdown(self, background_image: Image.Image, question: str, 
                                   answer: str, audio_path: str, question_data: dict) -> Optional[str]:
        """إنشاء فيديو مع عداد تنازلي"""
        
        try:
            # تحميل الصوت
            audio_clip = AudioFileClip(audio_path)
            audio_duration = audio_clip.duration
            
            # مدة الفيديو الكلية (الصوت + 3 ثوان للإجابة)
            total_duration = audio_duration + VIDEO_SETTINGS["answer_duration"]
            
            # إنشاء مقطع الصورة الأساسي
            bg_image_path = self.generated_videos_dir / f"temp_bg_{int(random.random() * 1000000)}.png"
            background_image.save(str(bg_image_path))
            
            image_clip = ImageClip(str(bg_image_path), duration=total_duration)
            
            # إنشاء نص السؤال
            question_clip = self._create_text_clip(
                text=question,
                duration=audio_duration,
                position='center',
                fontsize=60
            )
            
            # إنشاء عداد تنازلي
            countdown_clips = self._create_countdown_clips(
                duration=VIDEO_SETTINGS["question_duration"],
                start_time=0
            )
            
            # إنشاء نص الإجابة (تظهر في النهاية فقط)
            answer_clip = self._create_text_clip(
                text=f"Answer: {answer}",
                duration=VIDEO_SETTINGS["answer_duration"],
                position='center',
                fontsize=70,
                start_time=audio_duration
            )
            
            # إضافة نص تشجيعي
            encouragement_text = self._get_encouragement_text(question_data.get("difficulty", "medium"))
            encouragement_clip = self._create_text_clip(
                text=encouragement_text,
                duration=3,
                position='bottom',
                fontsize=40,
                start_time=2
            )
            
            # تجميع جميع المقاطع
            final_clip = CompositeVideoClip([
                image_clip,
                question_clip,
                answer_clip,
                encouragement_clip,
                *countdown_clips
            ])
            
            # إضافة الصوت
            final_clip = final_clip.set_audio(audio_clip)
            
            # حفظ الفيديو
            video_id = f"short_{int(random.random() * 1000000)}"
            video_path = self.generated_shorts_dir / f"{video_id}.mp4"
            
            final_clip.write_videofile(
                str(video_path),
                fps=VIDEO_SETTINGS["fps"],
                codec='libx264',
                audio_codec='aac',
                temp_audiofile=str(self.generated_videos_dir / f"temp_audio_{video_id}.m4a"),
                remove_temp=True
            )
            
            # تنظيف الملفات المؤقتة
            if bg_image_path.exists():
                bg_image_path.unlink()
            
            logger.info(f"Video created: {video_path}")
            return str(video_path)
            
        except Exception as e:
            logger.error(f"Error creating video: {e}")
            return None
    
    def _create_text_clip(self, text: str, duration: float, position: str = 'center',
                        fontsize: int = 60, start_time: float = 0) -> VideoClip:
        """إنشاء مقطع نصي"""
        
        # تقسيم النص الطويل إلى أسطر
        max_chars_per_line = 30
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= max_chars_per_line:
                current_line += " " + word if current_line else word
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        text_with_lines = "\n".join(lines)
        
        # إنشاء TextClip
        txt_clip = TextClip(
            text_with_lines,
            fontsize=fontsize,
            color='white',
            font='Arial-Bold',
            stroke_color='black',
            stroke_width=2,
            method='caption',
            size=(VIDEO_SETTINGS["resolution"][0] - 100, None),
            align='center'
        )
        
        # تحديد الموضع
        if position == 'top':
            y_pos = 150
        elif position == 'bottom':
            y_pos = VIDEO_SETTINGS["resolution"][1] - txt_clip.size[1] - 150
        else:  # center
            y_pos = (VIDEO_SETTINGS["resolution"][1] - txt_clip.size[1]) // 2
        
        txt_clip = txt_clip.set_position(('center', y_pos))
        txt_clip = txt_clip.set_duration(duration)
        txt_clip = txt_clip.set_start(start_time)
        
        return txt_clip
    
    def _create_countdown_clips(self, duration: int = 15, start_time: float = 0) -> List[VideoClip]:
        """إنشاء مقاطع للعداد التنازلي"""
        
        clips = []
        countdown_duration = 1  # مدة كل ثانية
        
        for second in range(duration, 0, -1):
            # إنشاء نص العداد
            countdown_text = f"{second}s"
            
            txt_clip = TextClip(
                countdown_text,
                fontsize=100,
                color='white',
                font='Arial-Bold',
                stroke_color='black',
                stroke_width=3,
                size=(200, 100),
                align='center'
            )
            
            # موضع العداد (أسفل المنتصف)
            y_pos = VIDEO_SETTINGS["resolution"][1] - 250
            txt_clip = txt_clip.set_position(('center', y_pos))
            txt_clip = txt_clip.set_duration(countdown_duration)
            txt_clip = txt_clip.set_start(start_time + (duration - second))
            
            # إضافة خلفية شفافة
            bg_clip = TextClip(
                "",
                fontsize=1,
                color='black',
                size=(250, 150),
                transparent=True
            )
            bg_clip = bg_clip.set_position(('center', y_pos - 25))
            bg_clip = bg_clip.set_duration(countdown_duration)
            bg_clip = bg_clip.set_start(start_time + (duration - second))
            bg_clip = bg_clip.set_opacity(0.5)
            
            clips.append(bg_clip)
            clips.append(txt_clip)
        
        return clips
    
    def _get_encouragement_text(self, difficulty: str) -> str:
        """الحصول على نص تشجيعي حسب الصعوبة"""
        
        texts = {
            "easy": [
                "You got this!",
                "Easy one!",
                "Think fast!"
            ],
            "medium": [
                "Challenge yourself!",
                "Can you solve it?",
                "Test your brain!"
            ],
            "hard": [
                "Only geniuses can solve this!",
                "Extremely difficult!",
                "Challenge accepted?"
            ]
        }
        
        return random.choice(texts.get(difficulty, texts["medium"]))
    
    def create_compilation_video(self, short_paths: List[str]) -> Optional[str]:
        """إنشاء فيديو تجميعي من الشورتات"""
        
        if len(short_paths) < 2:
            logger.warning("Need at least 2 shorts for compilation")
            return None
        
        try:
            # تحميل جميع الشورتات
            clips = []
            for i, short_path in enumerate(short_paths):
                if os.path.exists(short_path):
                    clip = VideoFileClip(short_path)
                    # إضافة انتقال بين الفيديوهات
                    if i > 0:
                        clip = clip.crossfadein(0.5)
                    clips.append(clip)
            
            if not clips:
                logger.error("No valid short videos found")
                return None
            
            # دمج جميع المقاطع
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # إضافة مقدمة ونهاية
            intro_duration = 2
            outro_duration = 3
            
            # إنشاء مقدمة
            intro_text = "Daily Brain Teasers\nCompilation"
            intro_clip = self._create_intro_clip(intro_text, intro_duration)
            
            # إنشاء نهاية
            outro_text = "Subscribe for more!\nNew puzzles every day!"
            outro_clip = self._create_outro_clip(outro_text, outro_duration)
            
            # تجميع الفيديو النهائي
            compilation_clip = concatenate_videoclips(
                [intro_clip, final_clip, outro_clip],
                method="compose"
            )
            
            # إضافة موسيقى خلفية للتجميع
            bg_music = self.audio_gen.get_background_music()
            if bg_music:
                try:
                    music_clip = AudioFileClip(bg_music)
                    # جعل الموسيقى تناسب طول الفيديو
                    if music_clip.duration < compilation_clip.duration:
                        # تكرار الموسيقى
                        music_clip = afx.audio_loop(music_clip, duration=compilation_clip.duration)
                    else:
                        music_clip = music_clip.subclip(0, compilation_clip.duration)
                    
                    # تقليل مستوى الموسيقى
                    music_clip = music_clip.volumex(0.3)
                    
                    # دمع الموسيقى مع الصوت الأصلي
                    final_audio = CompositeAudioClip([
                        compilation_clip.audio,
                        music_clip
                    ])
                    compilation_clip = compilation_clip.set_audio(final_audio)
                except Exception as e:
                    logger.error(f"Error adding background music: {e}")
            
            # حفظ الفيديو التجميعي
            compilation_id = f"compilation_{datetime.now().strftime('%Y%m%d')}"
            compilation_path = self.generated_videos_dir / f"{compilation_id}.mp4"
            
            compilation_clip.write_videofile(
                str(compilation_path),
                fps=VIDEO_SETTINGS["fps"],
                codec='libx264',
                audio_codec='aac'
            )
            
            logger.info(f"Compilation video created: {compilation_path}")
            return str(compilation_path)
            
        except Exception as e:
            logger.error(f"Error creating compilation video: {e}")
            return None
    
    def _create_intro_clip(self, text: str, duration: float) -> VideoClip:
        """إنشاء مقطع المقدمة"""
        
        # إنشاء خلفية
        bg_color = (41, 128, 185)  # أزرق
        bg_clip = ColorClip(
            size=VIDEO_SETTINGS["resolution"],
            color=bg_color,
            duration=duration
        )
        
        # إضافة نص
        txt_clip = TextClip(
            text,
            fontsize=80,
            color='white',
            font='Arial-Bold',
            stroke_color='black',
            stroke_width=3,
            size=(VIDEO_SETTINGS["resolution"][0] - 100, None),
            align='center',
            method='caption'
        )
        
        txt_clip = txt_clip.set_position('center')
        txt_clip = txt_clip.set_duration(duration)
        
        # تطبيق تأثير ظهور
        txt_clip = txt_clip.crossfadein(1)
        
        # تجميع
        intro_clip = CompositeVideoClip([bg_clip, txt_clip])
        
        return intro_clip
    
    def _create_outro_clip(self, text: str, duration: float) -> VideoClip:
        """إنشاء مقطع النهاية"""
        
        return self._create_intro_clip(text, duration)
    
    def _save_video_info(self, video_path: str, question_data: dict, image_source: str):
        """حفظ معلومات الفيديو"""
        
        info_file = Path(video_path).with_suffix('.json')
        info = {
            "video_path": video_path,
            "question": question_data["question"],
            "answer": question_data["answer"],
            "category": question_data.get("category", "general"),
            "difficulty": question_data.get("difficulty", "medium"),
            "image_source": image_source,
            "created_at": datetime.now().isoformat(),
            "question_id": question_data.get("question_id"),
            "source": question_data.get("source", "unknown")
        }
        
        import json
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)

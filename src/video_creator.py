import subprocess
from pathlib import Path
from typing import List, Dict
from datetime import datetime

from config.settings import *

class VideoCreator:
    def __init__(self):
        self.ffmpeg_path = self._find_ffmpeg()
    
    def create_short(self, background: Path, audio: Path, 
                    question_data: Dict, short_number: int) -> Path:
        """إنشاء شورت فيديو كامل"""
        output_path = OUTPUT_DIR / f"short_{datetime.now().strftime('%Y%m%d')}_{short_number}.mp4"
        
        # 1. إنشاء الفيديو الأساسي مع الخلفية
        temp_video = self._create_base_video(background, audio)
        
        # 2. إضافة نص السؤال
        video_with_text = self._add_question_text(temp_video, question_data)
        
        # 3. إضافة العداد
        video_with_countdown = self._add_countdown(video_with_text)
        
        # 4. إضافة الإجابة النهائية
        final_video = self._add_final_answer(video_with_countdown, question_data)
        
        # 5. التحسين النهائي
        self._optimize_video(final_video, output_path)
        
        # تنظيف الملفات المؤقتة
        for temp in [temp_video, video_with_text, video_with_countdown, final_video]:
            if temp.exists():
                temp.unlink()
        
        return output_path
    
    def create_compilation(self, shorts_data: List[Dict], day_date: str) -> Path:
        """إنشاء فيديو تجميعي"""
        output_path = OUTPUT_DIR / f"compilation_{datetime.now().strftime('%Y%m%d')}.mp4"
        
        # جمع مسارات الشورتات
        short_paths = [short["video_path"] for short in shorts_data]
        
        # قائمة ملفات لـ ffmpeg
        concat_file = TEMP_DIR / "concat_list.txt"
        
        with open(concat_file, 'w', encoding='utf-8') as f:
            for short in short_paths:
                f.write(f"file '{short.absolute()}'\n")
        
        # دمج الفيديوهات
        concat_cmd = [
            self.ffmpeg_path,
            '-f', 'concat',
            '-safe', '0',
            '-i', str(concat_file),
            '-c', 'copy',
            str(output_path)
        ]
        
        subprocess.run(concat_cmd, check=True, capture_output=True)
        
        # إضافة مقدمة وخاتمة
        final_video = self._add_compilation_intro_outro(output_path, day_date, len(shorts_data))
        
        return final_video
    
    def _add_question_text(self, video_path: Path, question_data: Dict) -> Path:
        """إضافة نص السؤال على الفيديو"""
        output_path = TEMP_DIR / f"with_text_{int(time.time())}.mp4"
        
        question = question_data["question"]
        # تقسيم السؤال إذا كان طويلاً
        if len(question) > 60:
            # إيجاد مكان مناسب للتقسيم
            middle = len(question) // 2
            split_point = question.rfind(' ', 0, middle)
            if split_point == -1:
                split_point = middle
            
            line1 = question[:split_point]
            line2 = question[split_point:].strip()
        else:
            line1 = question
            line2 = ""
        
        # استخدام ffmpeg لإضافة النص
        text_filter = (
            f"drawtext=text='{line1}':"
            f"fontcolor=white:fontsize=60:"
            f"box=1:boxcolor=black@0.5:boxborderw=10:"
            f"x=(w-text_w)/2:y=(h-text_h)/2-50"
        )
        
        if line2:
            text_filter += (
                f",drawtext=text='{line2}':"
                f"fontcolor=white:fontsize=50:"
                f"box=1:boxcolor=black@0.5:boxborderw=10:"
                f"x=(w-text_w)/2:y=(h-text_h)/2+50"
            )
        
        cmd = [
            self.ffmpeg_path,
            '-i', str(video_path),
            '-vf', text_filter,
            '-c:a', 'copy',
            str(output_path)
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path
    
    def _add_countdown(self, video_path: Path) -> Path:
        """إضافة عداد تنازلي"""
        output_path = TEMP_DIR / f"with_countdown_{int(time.time())}.mp4"
        
        # إنشاء عداد تنازلي
        countdown_filter = self._create_countdown_filter()
        
        cmd = [
            self.ffmpeg_path,
            '-i', str(video_path),
            '-vf', countdown_filter,
            '-c:a', 'copy',
            str(output_path)
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path
    
    def _add_final_answer(self, video_path: Path, question_data: Dict) -> Path:
        """إضافة الإجابة النهائية"""
        output_path = TEMP_DIR / f"with_answer_{int(time.time())}.mp4"
        
        # استخراج آخر 3 ثواني
        duration = self._get_video_duration(video_path)
        
        # تقسيم الفيديو إلى جزأين: قبل وبعد الإجابة
        temp1 = TEMP_DIR / "part1.mp4"
        temp2 = TEMP_DIR / "part2.mp4"
        
        # الجزء 1: حتى 3 ثواني قبل النهاية
        cmd1 = [
            self.ffmpeg_path,
            '-i', str(video_path),
            '-t', str(duration - 3),
            '-c', 'copy',
            str(temp1)
        ]
        
        # الجزء 2: إنشاء 3 ثواني مع الإجابة
        answer_text = f"Answer: {question_data['correct_answer']}"
        
        # إنشاء فيديو للإجابة
        answer_video = self._create_answer_video(answer_text, duration=3)
        
        # دمج الأجزاء
        concat_file = TEMP_DIR / "answer_concat.txt"
        with open(concat_file, 'w') as f:
            f.write(f"file '{temp1.absolute()}'\n")
            f.write(f"file '{answer_video.absolute()}'\n")
        
        cmd_final = [
            self.ffmpeg_path,
            '-f', 'concat',
            '-safe', '0',
            '-i', str(concat_file),
            '-c', 'copy',
            str(output_path)
        ]
        
        subprocess.run(cmd1, check=True, capture_output=True)
        subprocess.run(cmd_final, check=True, capture_output=True)
        
        # تنظيف
        for temp in [temp1, temp2, answer_video, concat_file]:
            if temp.exists():
                temp.unlink()
        
        return output_path
    
    def _create_answer_video(self, answer_text: str, duration: int = 3) -> Path:
        """إنشاء فيديو قصير للإجابة"""
        output_path = TEMP_DIR / f"answer_{int(time.time())}.mp4"
        
        # إنشاء خلفية سوداء
        cmd = [
            self.ffmpeg_path,
            '-f', 'lavfi',
            '-i', f'color=c=black:size={QUALITY_SETTINGS["video_resolution"][0]}x{QUALITY_SETTINGS["video_resolution"][1]}:d={duration}',
            '-vf', f"drawtext=text='{answer_text}':fontcolor=white:fontsize=80:x=(w-text_w)/2:y=(h-text_h)/2",
            '-c:a', 'aac',
            '-b:a', '192k',
            str(output_path)
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path

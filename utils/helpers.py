import os
import json
import random
import string
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path


def generate_unique_id(prefix: str = "", length: int = 8) -> str:
    """توليد معرف فريد"""
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    if prefix:
        return f"{prefix}_{timestamp}_{random_chars}"
    else:
        return f"{timestamp}_{random_chars}"


def ensure_directory(path: str) -> Path:
    """التأكد من وجود المجلد"""
    
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def clean_old_files(directory: str, max_age_hours: int = 24, 
                   extensions: List[str] = None):
    """تنظيف الملفات القديمة"""
    
    if extensions is None:
        extensions = ['.tmp', '.log', '.mp3', '.jpg', '.png']
    
    dir_path = Path(directory)
    if not dir_path.exists():
        return
    
    now = datetime.now()
    
    for file_path in dir_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in extensions:
            # حساب عمر الملف
            file_age = now - datetime.fromtimestamp(file_path.stat().st_mtime)
            
            if file_age.total_seconds() > max_age_hours * 3600:
                try:
                    file_path.unlink()
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")


def save_json(data: Any, filepath: str, indent: int = 2):
    """حفظ البيانات كملف JSON"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def load_json(filepath: str) -> Any:
    """تحميل البيانات من ملف JSON"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def format_duration(seconds: int) -> str:
    """تنسيق المدة الزمنية"""
    
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def get_file_size(filepath: str) -> str:
    """الحصول على حجم الملف بصيغة مقروءة"""
    
    size_bytes = os.path.getsize(filepath)
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.2f} TB"


def list_files(directory: str, pattern: str = "*") -> List[str]:
    """سرد الملفات في مجلد"""
    
    dir_path = Path(directory)
    if not dir_path.exists():
        return []
    
    return [str(f) for f in dir_path.glob(pattern) if f.is_file()]


def backup_file(source_path: str, backup_dir: str = "backups"):
    """إنشاء نسخة احتياطية للملف"""
    
    source = Path(source_path)
    if not source.exists():
        return None
    
    backup_path = ensure_directory(backup_dir)
    
    # إضافة timestamp للنسخة الاحتياطية
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{source.stem}_{timestamp}{source.suffix}"
    backup_file = backup_path / backup_name
    
    import shutil
    shutil.copy2(source_path, backup_file)
    
    return str(backup_file)


def validate_video_file(filepath: str) -> bool:
    """التحقق من صحة ملف الفيديو"""
    
    if not os.path.exists(filepath):
        return False
    
    # التحقق من الامتداد
    valid_extensions = ['.mp4', '.mov', '.avi', '.mkv']
    if Path(filepath).suffix.lower() not in valid_extensions:
        return False
    
    # التحقق من الحجم (لا يقل عن 100KB ولا يزيد عن 500MB)
    file_size = os.path.getsize(filepath)
    if file_size < 100 * 1024 or file_size > 500 * 1024 * 1024:
        return False
    
    return True


def truncate_text(text: str, max_length: int = 100, ellipsis: str = "...") -> str:
    """تقصير النص إذا كان طويلاً"""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(ellipsis)] + ellipsis


def get_random_element(items: List, weights: List[float] = None):
    """الحصول على عنصر عشوائي مع أوزان اختيارية"""
    
    if not items:
        return None
    
    if weights and len(weights) == len(items):
        return random.choices(items, weights=weights, k=1)[0]
    else:
        return random.choice(items)


def is_weekend() -> bool:
    """التحقق إذا كان اليوم عطلة نهاية الأسبوع"""
    
    today = datetime.now().weekday()  # 0 = Monday, 6 = Sunday
    return today >= 5  # Saturday or Sunday


def get_time_of_day() -> str:
    """الحصول على وقت اليوم"""
    
    hour = datetime.now().hour
    
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 22:
        return "evening"
    else:
        return "night"


def format_number(num: int) -> str:
    """تنسيق الأرقام"""
    
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return str(num)

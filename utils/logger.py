import logging
from pathlib import Path
from datetime import datetime

def setup_logger(name: str, log_file: Path, level=logging.INFO):
    """إعداد لوجر"""
    # إنشاء المجلد إذا لم يكن موجوداً
    log_file.parent.mkdir(exist_ok=True)
    
    # تهيئة الـ formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # إعداد الـ handler للفايل
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    # إعداد الـ handler للكونسول
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # إنشاء الـ logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # منع انتشار الـ logs
    logger.propagate = False
    
    return logger

class PerformanceLogger:
    """لوجر لقياس الأداء"""
    
    def __init__(self, task_name: str):
        self.task_name = task_name
        self.start_time = datetime.now()
        
    def start(self):
        """بدء المهمة"""
        self.start_time = datetime.now()
        print(f"⏳ بدء {self.task_name}...")
        
    def end(self):
        """إنهاء المهمة"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        print(f"✅ اكتمل {self.task_name} في {duration:.2f} ثانية")
        return duration

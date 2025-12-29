import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class CustomFormatter(logging.Formatter):
    """تنسيق مخصص لرسائل التسجيل"""
    
    # ألوان ANSI
    COLORS = {
        'DEBUG': '\033[94m',     # أزرق
        'INFO': '\033[92m',      # أخضر
        'WARNING': '\033[93m',   # أصفر
        'ERROR': '\033[91m',     # أحمر
        'CRITICAL': '\033[95m',  # بنفسجي
        'RESET': '\033[0m'       إعادة التعيين
    }
    
    def format(self, record):
        """تنسيق رسالة التسجيل"""
        
        # إضافة اللون لمستوى التسجيل
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        
        # إضافة timestamp
        record.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return super().format(record)


def setup_logger(name: str = "YouTubeAuto", 
                log_level: str = "INFO",
                log_to_file: bool = True,
                log_file: Optional[str] = None) -> logging.Logger:
    """إعداد وتسجيل"""
    
    # إنشاء logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # منع التكرار
    if logger.handlers:
        return logger
    
    # تنسيق الرسائل
    formatter = CustomFormatter(
        '%(timestamp)s - %(levelname)s - %(name)s - %(message)s'
    )
    
    # معالج وحدة التحكم
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # معالج الملف
    if log_to_file:
        if log_file is None:
            # إنشاء مجلد السجلات
            logs_dir = Path("logs")
            logs_dir.mkdir(exist_ok=True)
            
            # اسم الملف مع التاريخ
            date_str = datetime.now().strftime("%Y%m%d")
            log_file = logs_dir / f"youtube_auto_{date_str}.log"
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# إنشاء logger عام
logger = setup_logger()


def log_performance(start_time: datetime, operation: str):
    """تسجيل أداء العملية"""
    
    duration = (datetime.now() - start_time).total_seconds()
    logger.info(f"{operation} completed in {duration:.2f} seconds")


def log_error_with_context(error: Exception, context: dict = None):
    """تسجيل الخطأ مع السياق"""
    
    error_msg = f"Error: {type(error).__name__}: {str(error)}"
    
    if context:
        context_str = ", ".join(f"{k}={v}" for k, v in context.items())
        error_msg += f" | Context: {context_str}"
    
    logger.error(error_msg)


def log_system_status(status: dict):
    """تسجيل حالة النظام"""
    
    status_str = " | ".join(f"{k}: {v}" for k, v in status.items())
    logger.info(f"System Status: {status_str}")


def log_api_usage(api_name: str, success: bool, response_time: float = None):
    """تسجيل استخدام API"""
    
    status = "✓" if success else "✗"
    msg = f"API {api_name}: {status}"
    
    if response_time is not None:
        msg += f" ({response_time:.2f}s)"
    
    if success:
        logger.debug(msg)
    else:
        logger.warning(msg)


# دوال تسجيل مختصرة
def debug(msg: str, **kwargs):
    """تسجيل رسالة تصحيح"""
    logger.debug(msg, extra=kwargs)


def info(msg: str, **kwargs):
    """تسجيل رسالة معلومات"""
    logger.info(msg, extra=kwargs)


def warning(msg: str, **kwargs):
    """تسجيل رسالة تحذير"""
    logger.warning(msg, extra=kwargs)


def error(msg: str, **kwargs):
    """تسجيل رسالة خطأ"""
    logger.error(msg, extra=kwargs)


def critical(msg: str, **kwargs):
    """تسجيل رسالة حرجة"""
    logger.critical(msg, extra=kwargs)

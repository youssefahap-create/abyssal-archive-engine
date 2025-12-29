import requests
import random
import os
from typing import Optional, Tuple
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import io
import base64

from config.settings import BACKGROUNDS_DIR, GENERATED_DIR, VIDEO_SETTINGS
from config.secrets_manager import secrets_manager
from utils.logger import logger
from services.fallback_handler import FallbackHandler


class ImageGenerator:
    """فئة توليد الصور"""
    
    def __init__(self):
        self.fallback_handler = FallbackHandler()
        self.generated_images_dir = GENERATED_DIR / "images"
        self.generated_images_dir.mkdir(exist_ok=True)
        
        # تحميل الخلفيات المحلية
        self.backgrounds = self._load_backgrounds()
    
    def _load_backgrounds(self) -> list:
        """تحميل الخلفيات المحلية"""
        backgrounds = []
        if BACKGROUNDS_DIR.exists():
            for ext in ['.jpg', '.jpeg', '.png', '.webp']:
                backgrounds.extend(list(BACKGROUNDS_DIR.glob(f"*{ext}")))
        
        # إذا لم توجد خلفيات، إنشاء خلفيات ملونة
        if not backgrounds:
            logger.warning("No backgrounds found, creating colored backgrounds")
            self._create_default_backgrounds()
            backgrounds = list(BACKGROUNDS_DIR.glob("*.png"))
        
        return [str(bg) for bg in backgrounds]
    
    def _create_default_backgrounds(self):
        """إنشاء خلفيات ملونة افتراضية"""
        colors = [
            (41, 128, 185),  # أزرق
            (39, 174, 96),   # أخضر
            (142, 68, 173),  # بنفسجي
            (230, 126, 34),  # برتقالي
            (231, 76, 60),   # أحمر
            (52, 73, 94),    # رمادي داكن
            (26, 188, 156),  # تركواز
            (241, 196, 15),  # أصفر
        ]
        
        for i, color in enumerate(colors):
            img = Image.new('RGB', VIDEO_SETTINGS["resolution"], color)
            img_path = BACKGROUNDS_DIR / f"background_{i+1}.png"
            img.save(img_path)
        
        self.backgrounds = [str(BACKGROUNDS_DIR / f"background_{i+1}.png") 
                          for i in range(len(colors))]
    
    def get_background(self) -> Image.Image:
        """الحصول على خلفية عشوائية"""
        if not self.backgrounds:
            # إنشاء خلفية ملونة عشوائية
            color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
            return Image.new('RGB', VIDEO_SETTINGS["resolution"], color)
        
        bg_path = random.choice(self.backgrounds)
        try:
            image = Image.open(bg_path)
            image = image.resize(VIDEO_SETTINGS["resolution"])
            return image
        except Exception as e:
            logger.error(f"Error loading background {bg_path}: {e}")
            return Image.new('RGB', VIDEO_SETTINGS["resolution"], (41, 128, 185))
    
    def apply_blur(self, image: Image.Image, blur_intensity: int = None) -> Image.Image:
        """تطبيق تأثير بلور على الخلفية"""
        if blur_intensity is None:
            blur_intensity = VIDEO_SETTINGS["background_blur"]
        
        return image.filter(ImageFilter.GaussianBlur(blur_intensity))
    
    def generate_image_from_prompt(self, prompt: str) -> Optional[str]:
        """توليد صورة من وصف باستخدام نظام Fallback"""
        
        # استخدام نظام Fallback لتوليد الصور
        image_bytes = self.fallback_handler.generate_image(prompt)
        
        if image_bytes:
            # حفظ الصورة
            image_id = f"generated_{int(random.random() * 1000000)}"
            image_path = self.generated_images_dir / f"{image_id}.jpg"
            
            with open(image_path, 'wb') as f:
                f.write(image_bytes)
            
            logger.info(f"Image generated and saved: {image_path}")
            return str(image_path)
        
        return None
    
    def search_image(self, query: str) -> Optional[str]:
        """البحث عن صورة من الإنترنت"""
        
        # استخدام نظام Fallback للبحث عن الصور
        image_bytes = self.fallback_handler.search_image(query)
        
        if image_bytes:
            # حفظ الصورة
            image_id = f"searched_{int(random.random() * 1000000)}"
            image_path = self.generated_images_dir / f"{image_id}.jpg"
            
            with open(image_path, 'wb') as f:
                f.write(image_bytes)
            
            logger.info(f"Image downloaded and saved: {image_path}")
            return str(image_path)
        
        return None
    
    def get_image_for_question(self, question_data: dict) -> Tuple[Image.Image, str]:
        """الحصول على صورة مناسبة للسؤال"""
        
        prompt = question_data.get("image_prompt", "")
        category = question_data.get("category", "")
        
        # محاولة توليد صورة من الوصف
        image_path = self.generate_image_from_prompt(prompt)
        
        # إذا فشل التوليد، البحث عن صورة
        if not image_path:
            search_query = self._create_search_query(question_data)
            image_path = self.search_image(search_query)
        
        # إذا فشل البحث، استخدام خلفية مع نص
        if not image_path:
            logger.warning("Using background with text overlay")
            background = self.get_background()
            background = self.apply_blur(background)
            return background, "background"
        
        try:
            # تحميل الصورة المولدة
            image = Image.open(image_path)
            image = image.resize(VIDEO_SETTINGS["resolution"])
            
            # تطبيق بلور خفيف
            image = self.apply_blur(image, blur_intensity=5)
            
            return image, "generated"
            
        except Exception as e:
            logger.error(f"Error loading generated image: {e}")
            background = self.get_background()
            background = self.apply_blur(background)
            return background, "fallback"
    
    def _create_search_query(self, question_data: dict) -> str:
        """إنشاء استعلام بحث للصورة"""
        prompt = question_data.get("image_prompt", "")
        category = question_data.get("category", "")
        
        # تحسين استعلام البحث حسب الفئة
        if category == "flags":
            country = question_data.get("answer", "").split()[0]  # أخذ أول كلمة
            return f"{country} flag official"
        elif category == "landmarks":
            return f"{question_data.get('answer', '')} landmark"
        elif category == "animals":
            return f"{question_data.get('answer', '')} animal"
        else:
            # إزالة كلمات مثل "image of", "picture of"
            clean_prompt = prompt.lower()
            for word in ["image of", "picture of", "photo of", "visual for"]:
                clean_prompt = clean_prompt.replace(word, "").strip()
            
            return clean_prompt
    
    def create_text_overlay(self, image: Image.Image, text: str, 
                          font_size: int = 70, position: str = "center") -> Image.Image:
        """إضافة نص فوق الصورة"""
        draw = ImageDraw.Draw(image)
        
        # محاولة تحميل الخط، استخدام خط افتراضي إذا فشل
        try:
            font = ImageFont.truetype(VIDEO_SETTINGS["font_path"], font_size)
        except:
            font = ImageFont.load_default()
        
        # حساب حجم النص
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # حساب الموضع
        img_width, img_height = image.size
        
        if position == "center":
            x = (img_width - text_width) // 2
            y = (img_height - text_height) // 2
        elif position == "top":
            x = (img_width - text_width) // 2
            y = 100
        else:  # bottom
            x = (img_width - text_width) // 2
            y = img_height - text_height - 100
        
        # إضافة ظل للنص (اختياري)
        shadow_color = (0, 0, 0, 150)
        text_color = (255, 255, 255)
        
        # رسم الظل
        draw.text((x+2, y+2), text, font=font, fill=shadow_color)
        # رسم النص الرئيسي
        draw.text((x, y), text, font=font, fill=text_color)
        
        return image
    
    def create_countdown_overlay(self, image: Image.Image, seconds: int) -> Image.Image:
        """إضافة عداد تنازلي على الصورة"""
        draw = ImageDraw.Draw(image)
        
        # حجم الخط للعداد
        font_size = 100
        try:
            font = ImageFont.truetype(VIDEO_SETTINGS["font_path"], font_size)
        except:
            font = ImageFont.load_default()
        
        # نص العداد
        countdown_text = f"{seconds}s"
        
        # حساب الموضع (أسفل المنتصف)
        bbox = draw.textbbox((0, 0), countdown_text, font=font)
        text_width = bbox[2] - bbox[0]
        img_width, img_height = image.size
        
        x = (img_width - text_width) // 2
        y = img_height - 200  # 200 بكسيل من الأسفل
        
        # خلفية شبه شفافة للعداد
        padding = 20
        draw.rectangle(
            [x-padding, y-padding, x+text_width+padding, y+(bbox[3]-bbox[1])+padding],
            fill=(0, 0, 0, 128)  # أسود شفاف
        )
        
        # رسم النص
        draw.text((x, y), countdown_text, font=font, fill=(255, 255, 255))
        
        return image

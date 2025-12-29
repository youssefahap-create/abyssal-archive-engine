#!/usr/bin/env python3
"""
سكريبت إعداد المشروع للعمل مع GitHub Actions
"""
import os
import json
from pathlib import Path

def setup_for_github_actions():
    """تهيئة المشروع للعمل مع GitHub Actions"""
    
    print("🚀 Setting up project for GitHub Actions...")
    
    # 1. إنشاء مجلدات ضرورية
    directories = [
        ".github/workflows",
        "assets/backgrounds",
        "assets/local_images",
        "assets/local_audio",
        "assets/generated/images",
        "assets/generated/audio",
        "assets/generated/videos",
        "assets/generated/shorts",
        "assets/uploads",
        "database",
        "logs",
        "backups"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # 2. إنشاء ملف أسئلة محلية
    questions = [
        {
            "question": "What is the capital of France?",
            "answer": "Paris",
            "category": "general_knowledge",
            "difficulty": "easy",
            "image_prompt": "Eiffel Tower in Paris"
        },
        {
            "question": "How many continents are there?",
            "answer": "7",
            "category": "general_knowledge",
            "difficulty": "easy",
            "image_prompt": "World map with continents"
        },
        {
            "question": "What is the largest planet in our solar system?",
            "answer": "Jupiter",
            "category": "general_knowledge",
            "difficulty": "medium",
            "image_prompt": "Jupiter planet in space"
        }
    ]
    
    with open("assets/local_questions.json", "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    print("✅ Created local questions file")
    
    # 3. إنشاء خلفيات افتراضية
    try:
        from PIL import Image, ImageDraw
        
        colors = [
            (41, 128, 185),
            (39, 174, 96),
            (142, 68, 173),
            (230, 126, 34),
            (231, 76, 60),
        ]
        
        for i, color in enumerate(colors):
            img = Image.new('RGB', (1080, 1920), color)
            draw = ImageDraw.Draw(img)
            
            for x in range(0, 1080, 100):
                for y in range(0, 1920, 100):
                    if (x + y) % 200 == 0:
                        draw.rectangle([x, y, x+50, y+50], fill=(255, 255, 255, 50))
            
            img.save(f'assets/backgrounds/background_{i+1}.png')
        
        print(f"✅ Created {len(colors)} default backgrounds")
    except ImportError:
        print("⚠️  Could not create backgrounds (PIL not installed)")
    
    # 4. تحديث ملف .env.example ليتناسب مع GitHub Actions
    env_example = """# YouTube Auto Channel - GitHub Actions Version
# All secrets are loaded from GitHub Secrets automatically

# System Settings
LOG_LEVEL=INFO
TEST_MODE=false
GITHUB_ACTIONS=true
MAX_VIDEO_SIZE_MB=500
CLEANUP_OLD_FILES_DAYS=7
"""
    
    with open(".env.example", "w", encoding="utf-8") as f:
        f.write(env_example)
    print("✅ Updated .env.example for GitHub Actions")
    
    # 5. إنشاء ملف README إضافي للـ GitHub Actions
    readme_content = """# YouTube Auto Channel - GitHub Actions Edition

🎯 **يعمل تلقائياً 24/7 من GitHub بدون الحاجة لسيرفر!**

## 📅 جدولة التشغيل التلقائي

| الوقت (UTC) | المهمة | الوصف |
|------------|--------|-------|
| 06:00 | Daily Test | اختبار النظام اليومي |
| 07:00 | Daily Pipeline | توليد المحتوى اليومي كاملاً |
| 08:00 | Short 1 | الشورت الأول |
| 12:00 | Short 2 | الشورت الثاني |
| 16:00 | Short 3 | الشورت الثالث |
| 20:00 | Short 4 | الشورت الرابع |
| 22:00 | Compilation | الفيديو التجميعي |

## 🔧 كيف يعمل؟

1. **GitHub Actions** تستدعي Workflows حسب الجدول
2. **Workflows** تقوم بتنفيذ Python scripts
3. **المفاتيح** تُحمّل تلقائياً من GitHub Secrets
4. **الفيديوهات** تُرفع مباشرة إلى YouTube
5. **السجلات** تُحفظ كـ Artifacts لمدة 7 أيام

## 📊 المراقبة

1. **صفحة Actions:** لمشاهدة حالة التشغيل
2. **Artifacts:** لتحميل السجلات والملفات
3. **YouTube Channel:** لمشاهدة الفيديوهات المرفوعة
4. **Telegram:** للإشعارات (إذا أضفت Token)

## ⚙️ الإعداد

### 1. إضافة Secrets إلى GitHub:

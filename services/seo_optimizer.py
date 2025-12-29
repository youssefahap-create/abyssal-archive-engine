import random
from typing import List, Dict
from datetime import datetime

from utils.logger import logger


class SEOOptimizer:
    """محسن SEO للعناوين والأوصاف والهاشتاجات"""
    
    def __init__(self):
        self.templates = self._load_templates()
        self.hashtags_pool = self._create_hashtags_pool()
    
    def _load_templates(self) -> Dict:
        """تحميل قوالب SEO"""
        
        return {
            "titles": {
                "challenge": [
                    "Can YOU Solve This in 15 Seconds? {category} Challenge!",
                    "Only {percentage}% Can Answer This {category} Question!",
                    "Test Your {category} Knowledge in 15 Seconds!",
                    "Brain Teaser: {question_short}",
                    "{category} Quiz: Are You Smarter Than 95% of People?"
                ],
                "intrigue": [
                    "This {category} Question Will Blow Your Mind!",
                    "You Won't Believe The Answer to This {category} Question!",
                    "Mind-Blowing {category} Fact Revealed!",
                    "The {category} Question Everyone is Getting Wrong!"
                ],
                "simple": [
                    "{category} Question: {question_short}",
                    "Quick {category} Quiz: Can You Answer This?",
                    "{category} Trivia: Test Your Knowledge"
                ]
            },
            "descriptions": {
                "basic": """🧠 Test your knowledge in 15 seconds!
                
Question: {question}
                
Think you know the answer? Write it in the comments below! ⬇️
                
🔔 Subscribe for daily brain teasers!
📱 Follow for more challenges!
                
#brainteaser #quiz #trivia #generalknowledge #puzzle""",
                
                "detailed": """🎯 DAILY BRAIN TEASER 🎯
                
Challenge yourself with this {category} question! You have 15 seconds to answer.
                
❓ QUESTION: {question}
                
💭 THINK FAST: Can you solve it before time runs out?
                
👇 WRITE YOUR ANSWER in the comments below!
                
🏆 SCORE YOURSELF: 
- Answered in 5 seconds: Genius! 🧠
- Answered in 10 seconds: Very Smart! 👍
- Answered in 15 seconds: Good Job! ✅
- Couldn't answer: Try again tomorrow! 🔄
                
🔔 SUBSCRIBE for daily puzzles and brain teasers!
📲 SHARE with friends to challenge them!
                
#brainteaser #quiz #trivia #{category} #puzzle #knowledge #test #challenge"""
            }
        }
    
    def _create_hashtags_pool(self) -> Dict[str, List[str]]:
        """إنشاء مجموعة الهاشتاجات"""
        
        return {
            "general": [
                "#brainteaser", "#quiz", "#trivia", "#puzzle", "#riddle",
                "#generalknowledge", "#knowledge", "#test", "#challenge",
                "#mindgame", "#braingame", "#iqtest", "#smart"
            ],
            "flags": [
                "#flags", "#countries", "#geography", "#world", "#nation",
                "#countryflags", "#flagquiz", "#geographyquiz"
            ],
            "landmarks": [
                "#landmarks", "#monuments", "#travel", "#worldwonders",
                "#famousplaces", "#architecture", "#tourism"
            ],
            "animals": [
                "#animals", "#wildlife", "#nature", "#animalfacts",
                "#creatures", "#fauna", "#zoology"
            ],
            "trending": [
                "#viral", "#trending", "#shorts", "#shortsviral",
                "#youtubeshorts", "#viralshorts", "#fyp"
            ],
            "engagement": [
                "#comment", "#like", "#subscribe", "#share",
                "#engagement", "#community", "#interactive"
            ]
        }
    
    def generate_title(self, question_data: dict) -> str:
        """توليد عنوان محسن"""
        
        category = question_data.get("category", "general").replace("_", " ")
        question = question_data["question"]
        difficulty = question_data.get("difficulty", "medium")
        
        # اختصار السؤال إذا كان طويلاً
        question_short = question[:50] + "..." if len(question) > 50 else question
        
        # اختيار قالب حسب الصعوبة
        if difficulty == "hard":
            template_type = random.choice(["challenge", "intrigue"])
        elif difficulty == "easy":
            template_type = "simple"
        else:
            template_type = random.choice(["challenge", "simple"])
        
        # اختيار قالب عشوائي
        template = random.choice(self.templates["titles"][template_type])
        
        # ملء القالب
        title = template.format(
            category=category.title(),
            question_short=question_short,
            percentage=random.choice(["3", "5", "10", "15"]),
            difficulty=difficulty
        )
        
        # إضافة إيموجي
        emojis = {
            "general": "🧠",
            "flags": "🇺🇳",
            "landmarks": "🗺️",
            "animals": "🐘",
            "riddles": "❓",
            "trending": "🔥"
        }
        
        emoji = emojis.get(category.lower(), "🧠")
        title = f"{emoji} {title}"
        
        # تقليل الطول إذا زاد عن 100 حرف
        if len(title) > 100:
            title = title[:97] + "..."
        
        logger.info(f"Generated title: {title}")
        return title
    
    def generate_description(self, question_data: dict) -> str:
        """توليد وصف محسن"""
        
        category = question_data.get("category", "general").replace("_", " ")
        question = question_data["question"]
        
        # اختيار قالب الوصف
        use_detailed = random.choice([True, False])  # 50% فرصة لكل
        
        if use_detailed:
            template = self.templates["descriptions"]["detailed"]
        else:
            template = self.templates["descriptions"]["basic"]
        
        # ملء القالب
        description = template.format(
            category=category,
            question=question
        )
        
        # إضافة معلومات إضافية
        if use_detailed:
            description += self._get_additional_info(category)
        
        # إضافة طلب تفاعل
        description += "\n\n"
        description += self._get_engagement_prompt()
        
        logger.info(f"Generated description ({'detailed' if use_detailed else 'basic'} template)")
        return description
    
    def generate_tags(self, question_data: dict, max_tags: int = 15) -> List[str]:
        """توليد هاشتاجات"""
        
        category = question_data.get("category", "general")
        difficulty = question_data.get("difficulty", "medium")
        
        tags = []
        
        # إضافة هاشتاجات حسب الفئة
        category_key = category.lower() if category.lower() in self.hashtags_pool else "general"
        tags.extend(self.hashtags_pool[category_key][:5])
        
        # إضافة هاشتاجات عامة
        tags.extend(self.hashtags_pool["general"][:5])
        
        # إضافة هاشتاجات تفاعلية
        tags.extend(self.hashtags_pool["engagement"][:3])
        
        # إضافة هاشتاجات رائجة
        tags.extend(self.hashtags_pool["trending"][:3])
        
        # إضافة هاشتاجات حسب الصعوبة
        if difficulty == "hard":
            tags.extend(["#difficult", "#challenging", "#genius"])
        elif difficulty == "easy":
            tags.extend(["#easy", "#simple", "#beginner"])
        
        # إزالة التكرارات وتقليل العدد
        tags = list(dict.fromkeys(tags))[:max_tags]
        
        logger.info(f"Generated {len(tags)} tags")
        return tags
    
    def _get_additional_info(self, category: str) -> str:
        """الحصول على معلومات إضافية حسب الفئة"""
        
        info_snippets = {
            "general knowledge": """
📚 DID YOU KNOW?
The average person knows about 40,000 words, but only uses about 20,000 regularly.
                
✨ FUN FACT:
Learning new facts actually creates new neural pathways in your brain!""",
            
            "flags": """
🇺🇳 FLAG FACTS:
There are 195 countries in the world, each with a unique flag design.
                
🎨 COLOR MEANINGS:
Red often represents bravery, blue for peace, and green for nature.""",
            
            "landmarks": """
🗺️ TRAVEL TRIVIA:
The Great Wall of China is over 13,000 miles long!
                
🏛️ ARCHITECTURE:
Some ancient structures were built with such precision that we still don't know how they did it!""",
            
            "animals": """
🐾 ANIMAL KINGDOM:
There are over 8.7 million species of animals on Earth!
                
🌿 WILDLIFE:
The animal kingdom is full of incredible adaptations and survival strategies."""
        }
        
        return info_snippets.get(category.lower(), "")
    
    def _get_engagement_prompt(self) -> str:
        """الحصول على طلب تفاعل"""
        
        prompts = [
            "💬 COMMENT below with your answer and how long it took you!",
            "👇 WRITE YOUR ANSWER and tag a friend to challenge them!",
            "🗨️ LET'S DISCUSS! What was your answer? Comment below!",
            "🤔 THOUGHTS? Write your answer and reasoning in the comments!",
            "💭 WHAT DO YOU THINK? Share your answer below!",
            "👥 CHALLENGE A FRIEND! Tag them in the comments!",
            "🏆 HOW DID YOU SCORE? Let us know in the comments!",
            "📊 VOTE in the comments: Easy, Medium, or Hard?",
            "🎯 WANT MORE? Subscribe for daily challenges!",
            "🔔 TURN ON NOTIFICATIONS to never miss a puzzle!"
        ]
        
        return random.choice(prompts)
    
    def optimize_metadata(self, question_data: dict) -> Dict[str, str]:
        """تحسين جميع بيانات التعريف مرة واحدة"""
        
        return {
            "title": self.generate_title(question_data),
            "description": self.generate_description(question_data),
            "tags": self.generate_tags(question_data)
        }

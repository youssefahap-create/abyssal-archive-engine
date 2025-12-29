import json
import random
import requests
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import sqlite3

from config.settings import CONTENT_SETTINGS
from config.secrets_manager import secrets_manager
from utils.logger import logger
from services.fallback_handler import FallbackHandler


class ContentGenerator:
    """فئة توليد محتوى الأسئلة"""
    
    def __init__(self):
        self.fallback_handler = FallbackHandler()
        self.local_db = "database/questions.db"
        self._init_database()
        self._load_local_questions()
    
    def _init_database(self):
        """تهيئة قاعدة البيانات المحلية"""
        conn = sqlite3.connect(self.local_db)
        cursor = conn.cursor()
        
        # إنشاء جدول الأسئلة
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            category TEXT NOT NULL,
            difficulty TEXT DEFAULT 'medium',
            image_prompt TEXT,
            used BOOLEAN DEFAULT 0,
            used_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # جدول لأداء الأسئلة
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS question_performance (
            question_id INTEGER,
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            engagement_rate REAL DEFAULT 0,
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_local_questions(self):
        """تحميل الأسئلة المحلية من ملف JSON"""
        local_file = "assets/local_questions.json"
        try:
            with open(local_file, 'r', encoding='utf-8') as f:
                questions = json.load(f)
                
            conn = sqlite3.connect(self.local_db)
            cursor = conn.cursor()
            
            for q in questions:
                # التحقق من وجود السؤال
                cursor.execute(
                    "SELECT id FROM questions WHERE question = ?",
                    (q['question'],)
                )
                if not cursor.fetchone():
                    cursor.execute('''
                    INSERT INTO questions (question, answer, category, difficulty, image_prompt)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (q['question'], q['answer'], q['category'], 
                          q.get('difficulty', 'medium'), q.get('image_prompt', '')))
            
            conn.commit()
            conn.close()
            logger.info(f"Loaded {len(questions)} questions from local file")
            
        except FileNotFoundError:
            # إنشاء ملف الأسئلة المحلية إذا لم يوجد
            default_questions = [
                {
                    "question": "Which country's flag is red and white with a maple leaf?",
                    "answer": "Canada",
                    "category": "flags",
                    "difficulty": "easy",
                    "image_prompt": "Canadian flag with maple leaf"
                },
                {
                    "question": "What animal is known as the 'King of the Jungle'?",
                    "answer": "Lion",
                    "category": "animals",
                    "difficulty": "easy",
                    "image_prompt": "Lion in the jungle"
                }
            ]
            
            with open(local_file, 'w', encoding='utf-8') as f:
                json.dump(default_questions, f, indent=2)
            
            logger.info("Created default questions file")
    
    def generate_question(self, category: str = None) -> Dict:
        """توليد سؤال جديد"""
        # محاولة توليد سؤال جديد باستخدام AI
        ai_question = self._generate_ai_question(category)
        if ai_question:
            # حفظ السؤال في قاعدة البيانات
            self._save_question_to_db(ai_question)
            return ai_question
        
        # استخدام سؤال من قاعدة البيانات المحلية
        return self._get_local_question(category)
    
    def _generate_ai_question(self, category: str = None) -> Optional[Dict]:
        """توليد سؤال باستخدام الذكاء الاصطناعي"""
        
        # تحديد الفئة إذا لم يتم تحديدها
        if not category:
            category = random.choice(CONTENT_SETTINGS["content_types"])
        
        # إنشاء موجه للسؤال
        prompts = {
            "general_knowledge": "Create a general knowledge trivia question that can be answered in one word or short phrase. Include a fun fact. Format: Question: [question] Answer: [answer] Hint: [hint for image]",
            "flags": "Create a question about a country flag. Ask which country the flag belongs to. Format: Question: [question] Answer: [country] Hint: [description of flag]",
            "landmarks": "Create a question about a famous landmark or monument. Ask which country it's in or what it's called. Format: Question: [question] Answer: [answer] Hint: [landmark description]",
            "animals": "Create a question about an animal. Ask for its name or a fact about it. Format: Question: [question] Answer: [animal] Hint: [animal description]",
            "riddles": "Create a short riddle that can be solved in 15 seconds. Format: Question: [riddle] Answer: [answer] Hint: [visual hint]"
        }
        
        prompt = prompts.get(category, prompts["general_knowledge"])
        
        # استخدام نظام Fallback لتوليد المحتوى
        response = self.fallback_handler.generate_content(
            prompt=prompt,
            max_tokens=150
        )
        
        if response:
            try:
                # تحليل الاستجابة
                lines = response.split('\n')
                question = ""
                answer = ""
                hint = ""
                
                for line in lines:
                    if line.startswith("Question:"):
                        question = line.replace("Question:", "").strip()
                    elif line.startswith("Answer:"):
                        answer = line.replace("Answer:", "").strip()
                    elif line.startswith("Hint:"):
                        hint = line.replace("Hint:", "").strip()
                
                if question and answer:
                    return {
                        "question": question,
                        "answer": answer,
                        "category": category,
                        "image_prompt": hint or f"Visual representation of: {question}",
                        "difficulty": random.choice(["easy", "medium", "hard"]),
                        "source": "ai_generated"
                    }
            except Exception as e:
                logger.error(f"Error parsing AI response: {e}")
        
        return None
    
    def _get_local_question(self, category: str = None) -> Dict:
        """الحصول على سؤال من قاعدة البيانات المحلية"""
        conn = sqlite3.connect(self.local_db)
        cursor = conn.cursor()
        
        if category:
            cursor.execute('''
            SELECT id, question, answer, category, image_prompt 
            FROM questions 
            WHERE category = ? AND used = 0 
            ORDER BY RANDOM() 
            LIMIT 1
            ''', (category,))
        else:
            cursor.execute('''
            SELECT id, question, answer, category, image_prompt 
            FROM questions 
            WHERE used = 0 
            ORDER BY RANDOM() 
            LIMIT 1
            ''')
        
        result = cursor.fetchone()
        
        if result:
            question_id, question, answer, category, image_prompt = result
            
            # تحديث حالة السؤال كمستخدم
            cursor.execute('''
            UPDATE questions 
            SET used = 1, used_date = ?
            WHERE id = ?
            ''', (datetime.now().isoformat(), question_id))
            
            conn.commit()
            conn.close()
            
            return {
                "question": question,
                "answer": answer,
                "category": category,
                "image_prompt": image_prompt or f"Image for: {question}",
                "difficulty": "medium",
                "source": "local_database",
                "question_id": question_id
            }
        
        conn.close()
        
        # إذا لم توجد أسئلة، إنشاء سؤال افتراضي
        return self._create_default_question()
    
    def _save_question_to_db(self, question_data: Dict):
        """حفظ السؤال في قاعدة البيانات"""
        conn = sqlite3.connect(self.local_db)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO questions (question, answer, category, difficulty, image_prompt, used, used_date)
        VALUES (?, ?, ?, ?, ?, 1, ?)
        ''', (
            question_data["question"],
            question_data["answer"],
            question_data["category"],
            question_data.get("difficulty", "medium"),
            question_data.get("image_prompt", ""),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def _create_default_question(self) -> Dict:
        """إنشاء سؤال افتراضي"""
        default_questions = [
            {
                "question": "What is the capital of France?",
                "answer": "Paris",
                "category": "general_knowledge",
                "image_prompt": "Eiffel Tower in Paris",
                "difficulty": "easy"
            },
            {
                "question": "How many continents are there?",
                "answer": "7",
                "category": "general_knowledge",
                "image_prompt": "World map with continents",
                "difficulty": "easy"
            },
            {
                "question": "What is the largest planet in our solar system?",
                "answer": "Jupiter",
                "category": "general_knowledge",
                "image_prompt": "Jupiter planet in space",
                "difficulty": "medium"
            }
        ]
        
        question = random.choice(default_questions)
        question["source"] = "default"
        return question
    
    def get_trending_topics(self) -> List[str]:
        """الحصول على المواضيع الرائجة من Reddit"""
        try:
            # استخدام Reddit بدون API key (public endpoints)
            subreddits = ["todayilearned", "interestingasfuck", "Damnthatsinteresting", "educationalgifs"]
            subreddit = random.choice(subreddits)
            
            url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
            headers = {"User-Agent": "YouTubeAutoChannel/1.0"}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get("data", {}).get("children", [])
                
                topics = []
                for post in posts[:5]:
                    title = post.get("data", {}).get("title", "")
                    if title and len(title) < 100:
                        # تحويل المنشور إلى سؤال
                        question = self._convert_to_question(title)
                        if question:
                            topics.append(question)
                
                return topics[:3]  # إرجاع أفضل 3 مواضيع
            
        except Exception as e:
            logger.error(f"Error fetching trending topics: {e}")
        
        return []
    
    def _convert_to_question(self, fact: str) -> Optional[str]:
        """تحويل الحقيقة إلى سؤال"""
        # استخدام AI لتحويل الحقيقة إلى سؤال
        prompt = f"Convert this fact into a short trivia question that can be answered in one word: {fact}"
        
        response = self.fallback_handler.generate_content(
            prompt=prompt,
            max_tokens=50
        )
        
        if response and len(response) < 150:
            return response.strip()
        
        return None
    
    def generate_questions_for_day(self, count: int = 4) -> List[Dict]:
        """توليد أسئلة ليوم كامل"""
        questions = []
        categories_used = []
        
        for i in range(count):
            # اختيار فئة مختلفة لكل سؤال
            available_categories = [c for c in CONTENT_SETTINGS["content_types"] 
                                  if c not in categories_used]
            
            if not available_categories:
                available_categories = CONTENT_SETTINGS["content_types"]
                categories_used = []
            
            category = random.choice(available_categories)
            categories_used.append(category)
            
            # محاولة الحصول على مواضيع رائجة أولاً
            if i == 0:  # أول سؤال من المواضيع الرائجة
                trending = self.get_trending_topics()
                if trending:
                    question_text = random.choice(trending)
                    # إنشاء كائن سؤال من النص
                    question_data = {
                        "question": question_text,
                        "answer": "See comments",  # إجابة مفتوحة
                        "category": "trending",
                        "image_prompt": f"Visual for: {question_text}",
                        "difficulty": "medium",
                        "source": "trending"
                    }
                    questions.append(question_data)
                    continue
            
            # توليد سؤال عادي
            question = self.generate_question(category)
            questions.append(question)
        
        return questions

import random
import json
from datetime import datetime
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup
import re

from config.settings import *
from config.secrets_manager import SecretsManager

class ContentGenerator:
    def __init__(self, secrets_manager: SecretsManager):
        self.secrets = secrets_manager
        self.trending_topics = []
        self.last_trend_update = None
        
    def get_trending_topics(self, force_update=False):
        """الحصول على مواضيع ترند من مصادر مختلفة بدون API keys"""
        if (self.trending_topics and not force_update and 
            self.last_trend_update and 
            (datetime.now() - self.last_trend_update).hours < TREND_SETTINGS["update_frequency"]):
            return self.trending_topics
        
        topics = []
        
        try:
            # 1. من Reddit (بدون API)
            reddit_topics = self._scrape_reddit_trends()
            topics.extend(reddit_topics)
            
            # 2. من Google Trends (بدون API)
            google_topics = self._scrape_google_trends()
            topics.extend(google_topics)
            
            # 3. من Twitter Trends (بدون API - باستخدام Nitter)
            twitter_topics = self._scrape_twitter_trends()
            topics.extend(twitter_topics)
            
            # إزالة التكرارات
            unique_topics = []
            seen = set()
            for topic in topics:
                if topic.lower() not in seen:
                    seen.add(topic.lower())
                    unique_topics.append(topic)
            
            self.trending_topics = unique_topics[:20]  # احتفظ بـ 20 فقط
            self.last_trend_update = datetime.now()
            
        except Exception as e:
            print(f"⚠️  خطأ في جلب الترندات: {e}")
            
            # استخدام مواضيع احتياطية
            if not self.trending_topics:
                self.trending_topics = [
                    "Artificial Intelligence", "Space Exploration", "Climate Change",
                    "World History", "Geography Facts", "Scientific Discoveries",
                    "Animal Kingdom", "Human Body", "Technology Innovations",
                    "Cultural Traditions", "Famous Landmarks", "Country Flags",
                    "Ocean Mysteries", "Ancient Civilizations", "Modern Inventions"
                ]
        
        return self.trending_topics
    
    def _scrape_reddit_trends(self):
        """سحب ترندات من Reddit"""
        topics = []
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            
            # subreddits شعبية
            subreddits = ['todayilearned', 'interestingasfuck', 'science', 'history']
            
            for sub in subreddits:
                url = f"https://old.reddit.com/r/{sub}/"
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # استخراج العناوين
                    for post in soup.find_all('a', class_='title', href=True):
                        title = post.text.strip()
                        if title and len(title) > 10:
                            # تحسين العنوان ليكون سؤالاً
                            question = self._convert_to_question(title)
                            if question:
                                topics.append(question)
                    
                    # أخذ أول 5 مواضيع من كل subreddit
                    if len(topics) >= 5 * len(subreddits):
                        break
                        
        except Exception as e:
            print(f"⚠️  خطأ في سحب Reddit: {e}")
        
        return topics[:10]
    
    def _scrape_google_trends(self):
        """سحب ترندات من Google Trends"""
        topics = []
        try:
            url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'xml')
                
                for item in soup.find_all('title')[1:6]:  # تخطي العنوان الأول
                    title = item.text.strip()
                    if title:
                        question = self._convert_to_question(title)
                        if question:
                            topics.append(question)
                            
        except Exception as e:
            print(f"⚠️  خطأ في سحب Google Trends: {e}")
        
        return topics
    
    def _scrape_twitter_trends(self):
        """سحب ترندات من Twitter عبر Nitter"""
        topics = []
        try:
            url = "https://nitter.net"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                trend_section = soup.find('div', class_='trends')
                if trend_section:
                    for trend in trend_section.find_all('a', href=True)[:10]:
                        topic = trend.text.strip().replace('#', '')
                        if topic:
                            question = self._convert_to_question(topic)
                            if question:
                                topics.append(question)
                                
        except Exception as e:
            print(f"⚠️  خطأ في سحب Twitter Trends: {e}")
        
        return topics
    
    def _convert_to_question(self, topic: str) -> str:
        """تحويل الموضوع إلى سؤال"""
        topic_lower = topic.lower()
        
        question_templates = [
            "What do you know about {topic}?",
            "Can you identify this {topic}?",
            "Where can you find {topic}?",
            "When was {topic} discovered?",
            "How does {topic} work?",
            "Why is {topic} important?",
            "Which country is known for {topic}?",
            "What is the significance of {topic}?"
        ]
        
        # إزالة كلمات غير مهمة
        stop_words = ['the', 'a', 'an', 'this', 'that', 'these', 'those']
        words = [word for word in topic.split() if word.lower() not in stop_words]
        clean_topic = ' '.join(words[:5])  # أخذ أول 5 كلمات فقط
        
        if len(clean_topic.split()) < 2:
            return None
        
        template = random.choice(question_templates)
        return template.format(topic=clean_topic)
    
    def generate_question(self) -> Dict:
        """توليد سؤال كامل ببياناته"""
        question_type = random.choice(CONTENT_CONFIG["question_types"])
        difficulty = random.choice(CONTENT_CONFIG["difficulty_levels"])
        
        # استخدام AI إذا كان متاحاً، وإلا استخدام قاعدة محلية
        ai_question = self._generate_with_ai(question_type, difficulty)
        
        if ai_question:
            question_data = ai_question
        else:
            question_data = self._generate_local_question(question_type, difficulty)
        
        # إضافة بيانات إضافية
        question_data.update({
            "question_type": question_type,
            "difficulty": difficulty,
            "timestamp": datetime.now().isoformat(),
            "hashtags": self._generate_hashtags(question_type, difficulty)
        })
        
        return question_data
    
    def _generate_with_ai(self, q_type: str, difficulty: str) -> Optional[Dict]:
        """توليد سؤال باستخدام AI APIs"""
        # المحاولة مع Gemini أولاً
        gemini_key = self.secrets.get_key("gemini", "api")
        if gemini_key:
            try:
                return self._call_gemini_api(q_type, difficulty, gemini_key)
            except:
                self.secrets.mark_failed(self.secrets.active_keys.get("gemini"))
        
        # المحاولة مع OpenAI
        openai_key = self.secrets.get_key("openai", "api")
        if openai_key:
            try:
                return self._call_openai_api(q_type, difficulty, openai_key)
            except:
                self.secrets.mark_failed(self.secrets.active_keys.get("openai"))
        
        # المحاولة مع Groq
        groq_key = self.secrets.get_key("groq", "api")
        if groq_key:
            try:
                return self._call_groq_api(q_type, difficulty, groq_key)
            except:
                self.secrets.mark_failed("GROQ_API_KEY")
        
        return None
    
    def _call_gemini_api(self, q_type: str, difficulty: str, api_key: str) -> Dict:
        """استدعاء Gemini API"""
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""Generate a {difficulty} {q_type} question for YouTube Shorts with:
        1. A clear question text
        2. Correct answer
        3. 3 wrong answers for multiple choice
        4. Brief explanation (max 10 words)
        5. Image description for background
        
        Format as JSON:
        {{
            "question": "text",
            "correct_answer": "text",
            "wrong_answers": ["a", "b", "c"],
            "explanation": "text",
            "image_description": "text"
        }}"""
        
        response = model.generate_content(prompt)
        
        # تحليل الرد (هذا مثال مبسط، يحتاج معالجة حقيقية)
        return {
            "question": f"Sample {q_type} question?",
            "correct_answer": "Sample Answer",
            "wrong_answers": ["Wrong 1", "Wrong 2", "Wrong 3"],
            "explanation": "Brief explanation",
            "image_description": f"{q_type} related background image"
        }
    
    def _generate_local_question(self, q_type: str, difficulty: str) -> Dict:
        """توليد سؤال من قاعدة محلية"""
        # قاعدة أسئلة احتياطية
        questions_db = {
            "flag_identification": [
                {
                    "question": "Which country does this flag belong to?",
                    "correct_answer": "Japan",
                    "wrong_answers": ["China", "South Korea", "Thailand"],
                    "explanation": "Red circle on white background",
                    "image_description": "Japanese flag simple design"
                }
            ],
            "general_knowledge": [
                {
                    "question": "What is the largest planet in our solar system?",
                    "correct_answer": "Jupiter",
                    "wrong_answers": ["Saturn", "Neptune", "Earth"],
                    "explanation": "11 times wider than Earth",
                    "image_description": "Jupiter planet in space"
                }
            ],
            # ... إضافة المزيد من الأسئلة
        }
        
        if q_type in questions_db and questions_db[q_type]:
            return random.choice(questions_db[q_type])
        
        # سؤال افتراضي إذا لم يوجد
        return {
            "question": "What is the capital of France?",
            "correct_answer": "Paris",
            "wrong_answers": ["London", "Berlin", "Madrid"],
            "explanation": "City of Light in Europe",
            "image_description": "Eiffel Tower Paris landscape"
        }
    
    def _generate_hashtags(self, q_type: str, difficulty: str) -> List[str]:
        """توليد هاشتاجات مناسبة"""
        base_tags = ["Quiz", "Challenge", "TestYourBrain"]
        
        type_tags = {
            "flag_identification": ["Flags", "Countries", "Geography"],
            "general_knowledge": ["Trivia", "Knowledge", "Facts"],
            "landmark_recognition": ["Landmarks", "Travel", "World"],
            "country_from_image": ["Geography", "Countries", "Culture"]
        }
        
        difficulty_tags = {
            "easy": ["EasyQuiz", "FunFacts"],
            "medium": ["BrainTeaser", "ThinkFast"],
            "hard": ["GeniusTest", "HardChallenge"]
        }
        
        tags = base_tags + type_tags.get(q_type, []) + difficulty_tags.get(difficulty, [])
        return tags[:8]  # الحد إلى 8 هاشتاجات
    
    def generate_metadata(self, question_data: Dict, video_number: int) -> Dict:
        """توليد ميتاداتا كاملة للفيديو"""
        title = METADATA_TEMPLATES["title"].format(
            question_type=question_data["question_type"].replace("_", " ").title(),
            number=video_number,
            seconds=CHANNEL_CONFIG["countdown_duration"]
        )
        
        description = METADATA_TEMPLATES["description"].format(
            difficulty=question_data["difficulty"],
            seconds=CHANNEL_CONFIG["countdown_duration"],
            hashtags=" ".join([f"#{tag}" for tag in question_data["hashtags"][:5]])
        )
        
        # تحسين SEO للعناوين
        title = self._optimize_seo(title)
        
        return {
            "title": title,
            "description": description,
            "tags": METADATA_TEMPLATES["tags"] + question_data["hashtags"],
            "category": "28",  # تعليم
            "privacy": "private",  # سيتم جدولته
            "playlist_title": f"Daily Challenges {datetime.now().strftime('%B %Y')}"
        }
    
    def generate_compilation_metadata(self, shorts_count: int, day_date: str) -> Dict:
        """توليد ميتاداتا للفيديو التجميعي"""
        return {
            "title": f"🎯 {shorts_count} Brain Challenges in 1 Minute | {day_date}",
            "description": f"""Can you solve all {shorts_count} challenges? 
Test your knowledge with today's quiz compilation!

🔥 Daily quiz shorts
⏱ Quick brain exercises
🧠 Test your intelligence

#QuizCompilation #DailyChallenge #BrainWorkout #ShortsCompilation""",
            "tags": ["Compilation", "Quiz", "Challenge", "Shorts", "Daily"],
            "category": "28",
            "privacy": "private"
        }
    
    def _optimize_seo(self, title: str) -> str:
        """تحسين العنوان لـ SEO"""
        # إضافة كلمات مفتاحية
        keywords = ["Quiz", "Challenge", "Test", "Quick", "Brain", "Shorts"]
        
        words = title.split()
        if len(words) < 8:  # إذا كان العنوان قصيراً
            # إضافة كلمة مفتاحية غير موجودة
            for keyword in keywords:
                if keyword.lower() not in title.lower():
                    title = f"{title} | {keyword}"
                    break
        
        # ضبط الطول
        if len(title) > 70:
            title = title[:67] + "..."
        
        return title

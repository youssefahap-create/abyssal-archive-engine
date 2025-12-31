import random
from typing import Dict, List
from datetime import datetime
import emoji

from config import config
from core.logger import logger

class SEOOptimizer:
    def __init__(self):
        self.hashtags_pool = [
            "#quiz", "#challenge", "#trivia", "#test", "#knowledge",
            "#brainteaser", "#puzzle", "#riddle", "#fun", "#education",
            "#learning", "#mindgame", "#iqtest", "#smart", "#genius",
            "#viral", "#trending", "#foryou", "#shorts", "#youtubeshorts",
            "#dailyquiz", "#quickquiz", "#fastquiz", "#guess", "#identify"
        ]
        
        self.templates = {
            "title": [
                "Can You Answer This? {emoji}",
                "Quick Quiz Challenge! {emoji}",
                "Test Your Knowledge: {topic}",
                "Brain Teaser of the Day {emoji}",
                "Only 5% Get This Right! {emoji}",
                "Guess What This Is? {emoji}",
                "Daily Challenge: {topic}",
                "Are You Smart Enough? {emoji}"
            ],
            "description": [
                "Test your knowledge with this quick quiz! {emoji}\n\nWrite your answer in the comments below! 👇\n\nDon't forget to like and subscribe for daily challenges! 🔔\n\n{hashtags}",
                "Can you beat the timer? Challenge yourself with this quiz! {emoji}\n\nShare your answer with friends and see who's smarter! 🤔\n\nDaily quizzes at 12, 3, 6, and 9 PM! ⏰\n\n{hashtags}",
                "Think you're in the top 5%? Prove it with this challenge! {emoji}\n\nComment your answer below and let's see who gets it right! 💬\n\nNew quizzes every day! 📅\n\n{hashtags}",
                "Quick brain exercise! Can you identify this? {emoji}\n\nChallenge your friends and see who's the smartest! 🧠\n\nTurn on notifications so you don't miss daily quizzes! 🔔\n\n{hashtags}"
            ]
        }
    
    def generate_metadata(self, question_data: Dict, index: int) -> Dict:
        """Generate SEO optimized metadata for video"""
        
        topic = question_data.get("source_topic", "Quiz")
        question = question_data.get("question", "Quiz Question")
        question_type = question_data.get("question_type", "general")
        
        # Generate title
        title_template = random.choice(self.templates["title"])
        title = title_template.format(
            emoji=self._get_emoji(question_type),
            topic=topic[:50]
        )
        
        # Generate description
        desc_template = random.choice(self.templates["description"])
        hashtags = self._generate_hashtags(question_type, topic)
        description = desc_template.format(
            emoji=self._get_emoji(question_type),
            hashtags=hashtags
        )
        
        # Generate tags
        tags = self._generate_tags(question_type, topic)
        
        # Add call to action
        description += f"\n\n📢 Daily Quiz #{index+1}\n⏰ {datetime.now().strftime('%B %d, %Y')}"
        
        return {
            "title": title,
            "description": description,
            "tags": tags,
            "hashtags": hashtags,
            "category": config.YOUTUBE_CATEGORY_ID,
            "privacy_status": config.YOUTUBE_PRIVACY_STATUS
        }
    
    def generate_compilation_metadata(self, daily_shorts: List[Dict]) -> Dict:
        """Generate metadata for compilation video"""
        
        today = datetime.now().strftime("%B %d, %Y")
        
        title = f"Daily Quiz Compilation - {today} 🎯"
        
        description = f"""Today's quiz challenges all in one video! 🧠

Can you answer all of them? Test your knowledge with today's compilation!

Shorts included:
"""
        
        # Add each short description
        for i, short in enumerate(daily_shorts[:4]):
            description += f"\n{i+1}. {short.get('title', 'Quiz Challenge')}"
        
        description += f"""

Don't forget to like, comment, and subscribe for daily quizzes! 🔔

Follow for more:
✅ Daily shorts at 12, 3, 6, and 9 PM
✅ Compilation videos every day
✅ New challenges every time!

{self._generate_hashtags('compilation', 'daily')}
"""
        
        tags = [
            "compilation", "daily quiz", "quiz compilation",
            "challenge compilation", "brain teaser", "trivia",
            "knowledge test", "educational", "fun learning",
            "youtube shorts", "short videos", "viral content"
        ]
        
        return {
            "title": title,
            "description": description,
            "tags": tags,
            "hashtags": self._generate_hashtags('compilation', 'daily'),
            "category": config.YOUTUBE_CATEGORY_ID,
            "privacy_status": config.YOUTUBE_PRIVACY_STATUS
        }
    
    def _get_emoji(self, question_type: str) -> str:
        """Get relevant emoji for question type"""
        emoji_map = {
            "flag": "🇺🇳",
            "landmark": "🗽",
            "animal": "🐯",
            "science": "🔬",
            "history": "🏛️",
            "art": "🎨",
            "food": "🍕",
            "general": "🧠",
            "guess": "🤔",
            "identify": "🔍",
            "trivia": "📚",
            "compilation": "🎯"
        }
        
        return emoji_map.get(question_type, "🧠")
    
    def _generate_hashtags(self, question_type: str, topic: str) -> str:
        """Generate relevant hashtags"""
        
        type_hashtags = {
            "flag": ["#flags", "#countries", "#geography"],
            "landmark": ["#landmarks", "#travel", "#tourist"],
            "animal": ["#animals", "#wildlife", "#nature"],
            "science": ["#science", "#education", "#facts"],
            "history": ["#history", "#historical", "#facts"],
            "general": ["#quiz", "#challenge", "#trivia"]
        }
        
        # Get type-specific hashtags
        specific_tags = type_hashtags.get(question_type, ["#quiz", "#challenge"])
        
        # Add topic-specific hashtags
        topic_words = topic.lower().split()[:3]
        topic_tags = [f"#{word}" for word in topic_words if len(word) > 3]
        
        # Combine and select random
        all_tags = specific_tags + topic_tags + random.sample(self.hashtags_pool, 10)
        unique_tags = list(dict.fromkeys(all_tags))[:15]
        
        return " ".join(unique_tags)
    
    def _generate_tags(self, question_type: str, topic: str) -> List[str]:
        """Generate tags for YouTube"""
        
        base_tags = [
            "quiz", "challenge", "trivia", "test", "knowledge",
            "brain teaser", "puzzle", "riddle", "educational",
            "learning", "fun", "entertainment", "short", "shorts"
        ]
        
        type_tags = {
            "flag": ["flag", "country", "nation", "geography", "world"],
            "landmark": ["landmark", "monument", "tourist", "travel", "world"],
            "animal": ["animal", "wildlife", "nature", "creature", "biology"],
            "science": ["science", "facts", "education", "learning", "knowledge"],
            "history": ["history", "historical", "facts", "past", "events"],
            "general": ["general knowledge", "facts", "information", "learning"]
        }
        
        specific_tags = type_tags.get(question_type, [])
        
        # Add topic words
        topic_words = [word for word in topic.lower().split() if len(word) > 3][:5]
        
        # Combine all tags
        all_tags = base_tags + specific_tags + topic_words
        unique_tags = list(dict.fromkeys(all_tags))[:30]  # YouTube limit
        
        return unique_tags

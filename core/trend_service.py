import os
import random
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import praw
from pytrends.request import TrendReq
from newsapi import NewsApiClient
from tavily import TavilyClient

from config import config
from core.logger import logger

class TrendService:
    def __init__(self):
        self.reddit_client = None
        self.pytrends = None
        self.newsapi = None
        self.tavily = None
        
        # Initialize clients if API keys available
        try:
            if os.getenv("REDDIT_CLIENT_ID") and os.getenv("REDDIT_CLIENT_SECRET"):
                self.reddit_client = praw.Reddit(
                    client_id=os.getenv("REDDIT_CLIENT_ID"),
                    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                    user_agent="YouTubeAutomation/1.0"
                )
        except:
            pass
        
        try:
            self.pytrends = TrendReq(hl='en-US', tz=360)
        except:
            pass
        
        try:
            if os.getenv("NEWS_API"):
                self.newsapi = NewsApiClient(api_key=os.getenv("NEWS_API"))
        except:
            pass
        
        try:
            if os.getenv("TAVILY_API_KEY"):
                self.tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        except:
            pass
    
    def get_trending_topics(self, count: int = 10) -> List[Dict]:
        """Get trending topics from multiple sources"""
        all_topics = []
        
        for source in config.TREND_SOURCES:
            try:
                if source == "reddit" and self.reddit_client:
                    topics = self._get_reddit_trends()
                    all_topics.extend(topics)
                
                elif source == "googletrends" and self.pytrends:
                    topics = self._get_google_trends()
                    all_topics.extend(topics)
                
                elif source == "newsapi" and self.newsapi:
                    topics = self._get_news_trends()
                    all_topics.extend(topics)
                
                elif source == "tavily" and self.tavily:
                    topics = self._get_tavily_trends()
                    all_topics.extend(topics)
                    
            except Exception as e:
                logger.warning(f"Trend source {source} failed: {str(e)}")
                continue
        
        # Remove duplicates and shuffle
        unique_topics = []
        seen = set()
        for topic in all_topics:
            topic_str = f"{topic['title']}_{topic['source']}"
            if topic_str not in seen:
                seen.add(topic_str)
                unique_topics.append(topic)
        
        random.shuffle(unique_topics)
        return unique_topics[:count]
    
    def _get_reddit_trends(self) -> List[Dict]:
        """Get trending topics from Reddit"""
        topics = []
        
        try:
            # Get from popular subreddits
            subreddits = [
                "todayilearned", "AskReddit", "worldnews",
                "science", "technology", "history", "movies"
            ]
            
            for subreddit_name in subreddits:
                try:
                    subreddit = self.reddit_client.subreddit(subreddit_name)
                    
                    for post in subreddit.hot(limit=20):
                        if post.score > 100:  # Only popular posts
                            topics.append({
                                "title": post.title,
                                "description": post.selftext[:200] if post.selftext else "",
                                "source": "reddit",
                                "subreddit": subreddit_name,
                                "score": post.score,
                                "url": f"https://reddit.com{post.permalink}"
                            })
                except:
                    continue
        
        except Exception as e:
            logger.error(f"Reddit scraping failed: {str(e)}")
        
        return topics
    
    def _get_google_trends(self) -> List[Dict]:
        """Get trending topics from Google Trends"""
        topics = []
        
        try:
            # Get daily trends
            trending_searches = self.pytrends.trending_searches(pn='united_states')
            
            for idx, trend in trending_searches.head(20).iterrows():
                topics.append({
                    "title": str(trend[0]),
                    "description": f"Currently trending on Google",
                    "source": "google",
                    "rank": idx + 1,
                    "trend_score": 100 - idx
                })
        
        except Exception as e:
            logger.error(f"Google Trends failed: {str(e)}")
        
        return topics
    
    def _get_news_trends(self) -> List[Dict]:
        """Get trending news topics"""
        topics = []
        
        try:
            # Get top headlines
            headlines = self.newsapi.get_top_headlines(
                language='en',
                page_size=20
            )
            
            for article in headlines.get('articles', []):
                topics.append({
                    "title": article['title'],
                    "description": article['description'] or "",
                    "source": "news",
                    "url": article['url'],
                    "published_at": article['publishedAt']
                })
        
        except Exception as e:
            logger.error(f"NewsAPI failed: {str(e)}")
        
        return topics
    
    def _get_tavily_trends(self) -> List[Dict]:
        """Get trends using Tavily search"""
        topics = []
        
        try:
            # Search for trending topics
            response = self.tavily.search(
                query="trending topics today",
                max_results=10,
                include_raw_content=True
            )
            
            for result in response.get('results', []):
                topics.append({
                    "title": result['title'],
                    "description": result['content'][:200],
                    "source": "tavily",
                    "url": result['url'],
                    "score": result.get('score', 0)
                })
        
        except Exception as e:
            logger.error(f"Tavily failed: {str(e)}")
        
        return topics
    
    def convert_to_question(self, topic: Dict) -> Dict:
        """Convert trending topic to quiz question"""
        
        title = topic['title']
        source = topic['source']
        
        question_types = [
            ("flag", f"Which country's flag is associated with: {title}?"),
            ("landmark", f"Which famous landmark is related to: {title}?"),
            ("general", f"What is: {title}?"),
            ("guess", f"Can you guess what this is about: {title}?"),
            ("identify", f"Identify the subject of: {title}"),
            ("trivia", f"Trivia question about: {title}")
        ]
        
        # Select question type based on topic content
        question_type, question_template = random.choice(question_types)
        
        # Generate actual question
        if "country" in title.lower() or "nation" in title.lower():
            question = f"Which country is mentioned in: {title}?"
            answer = self._extract_country(title)
        elif "city" in title.lower() or "capital" in title.lower():
            question = f"Which city is referenced in: {title}?"
            answer = title.split()[0]  # Simple extraction
        else:
            question = random.choice(config.QUESTION_TEMPLATES)
            answer = title
        
        return {
            "question": question,
            "answer": answer or "Check comments for answer",
            "question_type": question_type,
            "source_topic": title,
            "source": source,
            "difficulty": random.choice(["easy", "medium", "hard"])
        }
    
    def _extract_country(self, text: str) -> Optional[str]:
        """Extract country name from text"""
        import pycountry
        
        words = text.split()
        for word in words:
            word_clean = ''.join(c for c in word if c.isalpha())
            if len(word_clean) > 2:
                try:
                    country = pycountry.countries.lookup(word_clean)
                    return country.name
                except:
                    continue
        
        return None

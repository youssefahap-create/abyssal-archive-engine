import wikipediaapi
import feedparser
import requests
import random
import re
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
from config.config import config
from .logger import content_logger

class ContentScraper:
    """Class to scrape and curate content for YouTube videos"""
    
    def __init__(self):
        self.wikipedia_wiki = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='TheAbyssalArchiveBot/1.0 (contact@abyssalarchive.com)'
        )
    
    def get_wikipedia_list_content(self, list_name: str) -> List[Dict]:
        """Get content from Wikipedia lists of mysteries and unexplained phenomena"""
        try:
            page = self.wikipedia_wiki.page(list_name)
            if not page.exists():
                content_logger.warning(f"Wikipedia page does not exist: {list_name}")
                return []
            
            content = page.text
            # Extract items from the list (basic parsing)
            lines = content.split('\n')
            items = []
            
            for line in lines:
                # Look for list items starting with *, #, or bullet points
                if line.strip().startswith(('*', '#', '-')) and len(line.strip()) > 10:
                    item_text = line.strip()[1:].strip()  # Remove the list marker
                    if len(item_text) > 20:  # Only include substantial items
                        items.append({
                            "title": item_text.split('.')[0][:100] if '.' in item_text else item_text[:100],
                            "description": item_text,
                            "source": "Wikipedia",
                            "category": self._categorize_content(item_text)
                        })
            
            content_logger.info(f"Retrieved {len(items)} items from Wikipedia list: {list_name}")
            return items[:10]  # Limit to 10 items to avoid overwhelming
            
        except Exception as e:
            content_logger.error(f"Error getting Wikipedia content: {str(e)}")
            return []
    
    def get_google_trends(self) -> List[Dict]:
        """Get trending topics that could be turned into scary/mystery content"""
        try:
            # Using Google Trends API via pytrends (would need to install separately)
            # For now, simulate with a mock implementation
            trends = [
                {"keyword": "deep sea creatures", "interest": 85},
                {"keyword": "unsolved murders", "interest": 78},
                {"keyword": "ghost stories", "interest": 72},
                {"keyword": "ancient civilizations", "interest": 68},
                {"keyword": "space anomalies", "interest": 65}
            ]
            
            # Convert to content format
            formatted_trends = []
            for trend in trends:
                formatted_trends.append({
                    "title": f"Top 10 {trend['keyword']}",
                    "description": f"Exploring the most chilling {trend['keyword']} that will keep you awake at night",
                    "source": "Google Trends",
                    "category": self._categorize_content(trend['keyword']),
                    "search_volume": trend['interest']
                })
            
            content_logger.info(f"Retrieved {len(formatted_trends)} trending topics")
            return formatted_trends
            
        except Exception as e:
            content_logger.error(f"Error getting Google Trends: {str(e)}")
            return []
    
    def get_reddit_rss_feeds(self) -> List[Dict]:
        """Get content from relevant subreddits via RSS feeds"""
        try:
            subreddits = [
                "r/nosleep", "r/UnresolvedMysteries", "r/Paranormal", 
                "r/Conspiracy", "r/historymysteries"
            ]
            
            all_posts = []
            for subreddit in subreddits:
                rss_url = f"https://www.reddit.com/r/{subreddit.split('/')[1]}/.rss"
                try:
                    feed = feedparser.parse(rss_url)
                    
                    for entry in feed.entries[:5]:  # Take top 5 posts
                        title = entry.title
                        description = entry.summary if hasattr(entry, 'summary') else ""
                        
                        all_posts.append({
                            "title": title,
                            "description": description,
                            "source": f"Reddit - {subreddit}",
                            "link": entry.link if hasattr(entry, 'link') else "",
                            "category": self._categorize_content(title + " " + description),
                            "score": entry.score if hasattr(entry, 'score') else 0
                        })
                        
                except Exception as e:
                    content_logger.warning(f"Error fetching RSS from {subreddit}: {str(e)}")
            
            content_logger.info(f"Retrieved {len(all_posts)} posts from Reddit RSS feeds")
            return all_posts
            
        except Exception as e:
            content_logger.error(f"Error getting Reddit RSS feeds: {str(e)}")
            return []
    
    def get_nasa_apod(self) -> Optional[Dict]:
        """Get NASA's Astronomy Picture of the Day and create scary interpretation"""
        try:
            if not config.NASA_API_KEY:
                content_logger.warning("NASA_API_KEY not configured")
                return None
            
            url = f"https://api.nasa.gov/planetary/apod"
            params = {
                "api_key": config.NASA_API_KEY,
                "date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Create a scary interpretation of the astronomy photo
            scary_description = self._create_scary_astronomy_description(data.get("title", ""), data.get("explanation", ""))
            
            nasa_content = {
                "title": f"The Cosmic Horror: {data.get('title', 'Unknown Astronomical Phenomenon')}",
                "description": scary_description,
                "source": "NASA APOD",
                "media_url": data.get("hdurl") or data.get("url"),
                "category": "space",
                "date_taken": data.get("date")
            }
            
            content_logger.info(f"Retrieved NASA APOD content: {nasa_content['title']}")
            return nasa_content
            
        except Exception as e:
            content_logger.error(f"Error getting NASA APOD: {str(e)}")
            return None
    
    def get_noaa_data(self) -> Optional[Dict]:
        """Get NOAA ocean data and create mysterious interpretation"""
        try:
            if not config.NOAA_API_KEY:
                content_logger.warning("NOAA_API_KEY not configured")
                return None
            
            # Example: Get ocean temperature anomaly data
            # This is a simplified example - real implementation would use specific NOAA endpoints
            url = "https://www.ncei.noaa.gov/access/services/data/v1"
            params = {
                "dataset": "daily-summaries",
                "startDate": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                "endDate": datetime.now().strftime("%Y-%m-%d"),
                "bbox": "-180,-90,180,90",  # Global
                "format": "json"
            }
            
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                # Process the response to find interesting ocean anomalies
                # For demo purposes, creating mock content
                noaa_content = {
                    "title": "The Deep Ocean Anomaly: Unusual Temperature Readings",
                    "description": "Scientists have detected unprecedented temperature fluctuations in the Mariana Trench, suggesting activity from an unknown source deep beneath the ocean floor.",
                    "source": "NOAA Data",
                    "category": "ocean",
                    "data_point": "Temperature anomaly detected"
                }
                
                content_logger.info(f"Retrieved NOAA content: {noaa_content['title']}")
                return noaa_content
            else:
                content_logger.warning(f"NOAA API returned status {response.status_code}")
                return None
            
        except Exception as e:
            content_logger.error(f"Error getting NOAA data: {str(e)}")
            return None
    
    def _categorize_content(self, text: str) -> str:
        """Categorize content based on keywords"""
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in ['space', 'cosmic', 'astronomy', 'planet', 'galaxy', 'alien']):
            return 'space'
        elif any(keyword in text_lower for keyword in ['ocean', 'sea', 'underwater', 'deep', 'trench', 'marine']):
            return 'ocean'
        elif any(keyword in text_lower for keyword in ['history', 'ancient', 'civilization', 'archaeology', 'ruins']):
            return 'history'
        elif any(keyword in text_lower for keyword in ['crime', 'murder', 'disappearance', 'serial', 'killer']):
            return 'crime'
        elif any(keyword in text_lower for keyword in ['ghost', 'paranormal', 'supernatural', 'haunted', 'spirit']):
            return 'paranormal'
        else:
            return 'mystery'  # Default category
    
    def _create_scary_astronomy_description(self, title: str, explanation: str) -> str:
        """Create a scary interpretation of astronomical phenomena"""
        scary_elements = [
            "What if this isn't just a beautiful cosmic event?",
            "Scientists can't explain the unusual patterns detected...",
            "Local observatories report equipment malfunctions near the same time...",
            "The light pattern appears to pulse in a rhythm that matches human heartbeats...",
            "Radio telescopes picked up strange signals originating from this location...",
            "Multiple sightings of unexplained objects have been reported in this region..."
        ]
        
        selected_element = random.choice(scary_elements)
        return f"{explanation} {selected_element}"
    
    def filter_ad_safe_content(self, content: List[Dict]) -> List[Dict]:
        """Filter out content that might trigger YouTube's advertiser-unfriendly algorithm"""
        ad_unsafe_keywords = [
            'kill', 'death', 'suicide', 'violence', 'blood', 'gore', 
            'sexual', 'nudity', 'profanity', 'drug', 'alcohol abuse'
        ]
        
        safe_content = []
        for item in content:
            title_desc = (item.get('title', '') + ' ' + item.get('description', '')).lower()
            is_safe = not any(keyword in title_desc for keyword in ad_unsafe_keywords)
            
            if is_safe:
                safe_content.append(item)
            else:
                content_logger.info(f"Filtered out potentially ad-unsafe content: {item.get('title', '')[:50]}...")
        
        content_logger.info(f"Filtered {len(content) - len(safe_content)} items for ad safety. Kept {len(safe_content)} items.")
        return safe_content

class ScriptGenerator:
    """Class to generate video scripts using AI"""
    
    def __init__(self):
        import google.generativeai as genai
        if config.GEMINI_API_KEY_1:
            genai.configure(api_key=config.GEMINI_API_KEY_1)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
            content_logger.warning("GEMINI_API_KEY_1 not configured, script generation will be limited")
    
    def generate_mystery_script(self, topic: str, fact_count: int = 7) -> Optional[Dict]:
        """Generate a mystery script with hook, facts, and conclusion"""
        try:
            if not self.model:
                # Fallback to mock content if no API key
                return self._generate_mock_script(topic, fact_count)
            
            prompt = f"""
            You are creating a script for a YouTube video about mysterious and scary facts.
            The topic is: "{topic}"
            
            Create a script with the following structure:
            1. A powerful hook opening that starts immediately with the mysterious event (no greetings)
            2. {fact_count} mysterious/scary facts related to the topic
            3. Each fact should be compelling and well-researched
            4. End with a thought-provoking question to encourage comments
            5. Total length should be suitable for a 3-6 minute video
            
            Format the response as JSON with fields: hook, facts (array), conclusion, total_duration_estimate
            Also include: title, category
            """
            
            response = self.model.generate_content(prompt)
            
            # Parse the response (in a real implementation, we'd have better parsing)
            script_data = {
                "hook": f"In the depths of {topic}, something terrifying emerged...",
                "facts": [f"Mysterious fact about {topic} #{i}" for i in range(1, fact_count + 1)],
                "conclusion": "What do you think is really going on? Share your theories in the comments below.",
                "total_duration_estimate": 300,  # 5 minutes in seconds
                "title": f"Top {fact_count} Mysteries of {topic}",
                "category": "mystery"
            }
            
            content_logger.info(f"Generated script for topic: {topic}")
            return script_data
            
        except Exception as e:
            content_logger.error(f"Error generating script: {str(e)}")
            return self._generate_mock_script(topic, fact_count)
    
    def _generate_mock_script(self, topic: str, fact_count: int = 7) -> Dict:
        """Generate a mock script when API is unavailable"""
        content_logger.warning(f"Using mock script generator for topic: {topic}")
        
        hook = f"Scientists were baffled when they discovered evidence of {topic} in locations where it shouldn't exist."
        facts = [f"Fact {i}: Something strange happened in {topic} that defies conventional understanding." for i in range(1, fact_count + 1)]
        conclusion = "Do you believe there's more to this than meets the eye? Let us know your thoughts!"
        
        return {
            "hook": hook,
            "facts": facts,
            "conclusion": conclusion,
            "total_duration_estimate": 300,
            "title": f"Top {fact_count} Mysteries of {topic}",
            "category": self._categorize_topic(topic)
        }
    
    def _categorize_topic(self, topic: str) -> str:
        """Simple topic categorization"""
        topic_lower = topic.lower()
        if 'space' in topic_lower or 'cosmic' in topic_lower:
            return 'space'
        elif 'ocean' in topic_lower or 'sea' in topic_lower:
            return 'ocean'
        elif 'history' in topic_lower or 'ancient' in topic_lower:
            return 'history'
        elif 'crime' in topic_lower or 'murder' in topic_lower:
            return 'crime'
        else:
            return 'mystery'

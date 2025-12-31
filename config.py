import os
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Config:
    # Paths
    BASE_DIR: Path = Path(__file__).parent
    STORAGE_DIR: Path = BASE_DIR / "storage"
    LOGS_DIR: Path = BASE_DIR / "logs"
    ASSETS_DIR: Path = BASE_DIR / "assets"
    
    # Video settings
    SHORT_DURATION: int = 15
    ANSWER_DURATION: int = 3
    VIDEO_WIDTH: int = 1080
    VIDEO_HEIGHT: int = 1920
    FPS: int = 30
    BACKGROUND_COLOR: str = "#1a1a2e"
    TEXT_COLOR: str = "#ffffff"
    SECONDARY_COLOR: str = "#0f3460"
    ACCENT_COLOR: str = "#e94560"
    
    # Content settings
    DAILY_SHORTS_COUNT: int = 4
    COMPILATION_VIDEO_COUNT: int = 4
    QUESTION_TEMPLATES: List[str] = None
    MOTIVATIONAL_PHRASES: List[str] = None
    
    # Font settings
    FONT_PATH: Path = ASSETS_DIR / "fonts" / "Roboto-Bold.ttf"
    FONT_SIZE_TITLE: int = 80
    FONT_SIZE_QUESTION: int = 60
    FONT_SIZE_TIMER: int = 100
    
    # TTS Providers order
    TTS_PROVIDERS: List[str] = None
    
    # Image providers order
    IMAGE_PROVIDERS: List[str] = None
    
    # Trend sources
    TREND_SOURCES: List[str] = None
    
    # YouTube settings
    YOUTUBE_CATEGORY_ID: str = "22"
    YOUTUBE_PRIVACY_STATUS: str = "public"
    
    # Publishing times (UTC)
    PUBLISHING_TIMES: List[str] = ["12:00", "15:00", "18:00", "21:00"]
    
    # Cache settings
    MAX_CACHE_DAYS: int = 7
    
    def __post_init__(self):
        if self.QUESTION_TEMPLATES is None:
            self.QUESTION_TEMPLATES = [
                "Which country's flag is this?",
                "Guess this famous landmark",
                "What is this object?",
                "Which famous person is this?",
                "Identify this animal",
                "What is this scientific term?",
                "Which historical event is depicted?",
                "Name this musical instrument",
                "What is this chemical element?",
                "Which planet is this?"
            ]
        
        if self.MOTIVATIONAL_PHRASES is None:
            self.MOTIVATIONAL_PHRASES = [
                "If you know the answer fast, you are in the top 5% smartest people",
                "Write your answer in the comments below!",
                "Test your knowledge with this challenge",
                "Can you beat the timer?",
                "Share your answer with friends!"
            ]
        
        if self.TTS_PROVIDERS is None:
            self.TTS_PROVIDERS = ["elevenlabs", "groq", "openai", "gtts", "pyttsx3"]
        
        if self.IMAGE_PROVIDERS is None:
            self.IMAGE_PROVIDERS = ["pexels", "unsplash", "pixabay", "freepik", "vecteezy", "local"]
        
        if self.TREND_SOURCES is None:
            self.TREND_SOURCES = ["reddit", "googletrends", "newsapi", "tavily"]
    
    @property
    def today_str(self) -> str:
        return datetime.now().strftime("%Y%m%d")
    
    @property
    def timestamp_str(self) -> str:
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def setup_directories(self):
        """Create all necessary directories"""
        directories = [
            self.STORAGE_DIR,
            self.LOGS_DIR,
            self.ASSETS_DIR,
            self.STORAGE_DIR / "audio",
            self.STORAGE_DIR / "images",
            self.STORAGE_DIR / "videos",
            self.STORAGE_DIR / "shorts",
            self.STORAGE_DIR / "compilations",
            self.STORAGE_DIR / "thumbnails",
            self.ASSETS_DIR / "fonts",
            self.ASSETS_DIR / "backgrounds",
            self.ASSETS_DIR / "templates",
            self.ASSETS_DIR / "cache",
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Download default font if not exists
        if not self.FONT_PATH.exists():
            self._download_default_font()
    
    def _download_default_font(self):
        """Download Roboto font if not available"""
        import requests
        
        font_url = "https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"
        try:
            response = requests.get(font_url)
            # This is simplified - actual font downloading would be more complex
            # For production, include font file in repository
            pass
        except:
            pass

config = Config()

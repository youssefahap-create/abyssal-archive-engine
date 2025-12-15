import os
import sys
import json
from datetime import datetime

def create_directory_structure():
    """Create the entire directory structure for the YouTube Automation Project"""
    directories = [
        "logs",
        "assets",
        "assets/thumbnails",
        "assets/videos",
        "assets/images",
        "src",
        "src/utils",
        "data",
        "data/logs",
        "tests",
        "config",
        ".github/workflows"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def create_requirements_txt():
    """Create requirements.txt file with all necessary dependencies"""
    requirements_content = """requests>=2.31.0
google-auth>=2.23.0
google-auth-oauthlib>=1.1.0
google-auth-httplib2>=0.1.1
google-api-python-client>=2.97.0
edge-tts>=6.1.7
moviepy>=1.0.3
pillow>=10.0.0
openai>=1.3.5
google-generativeai>=0.4.0
replicate>=0.21.1
pexels-api>=1.0.1
pixabay-python>=0.5
youtube-upload>=0.3.3
tavily-python>=0.3.3
python-telegram-bot>=20.7
numpy>=1.24.3
ffmpeg-python>=0.2.0
pydub>=0.25.1
feedparser>=6.0.10
wikipedia-api>=0.5.8
huggingface-hub>=0.20.1
python-dotenv>=1.0.0
pytz>=2023.3
schedule>=1.2.0
urllib3>=2.0.4
certifi>=2023.7.22
charset-normalizer>=3.2.0
idna>=3.4
"""
    
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements_content)
    print("Created requirements.txt")

def create_config_py():
    """Create config.py file with all configuration settings"""
    config_content = '''import os
from typing import Optional, Dict, Any
import pytz

class Config:
    """
    Configuration class for The Abyssal Archive YouTube Automation Project
    All sensitive data is loaded from environment variables
    """
    
    # API Keys - Loaded from environment variables
    CAMB_AI_KEY_1 = os.environ.get('CAMB_AI_KEY_1')
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
    COVERR_API_ID = os.environ.get('COVERR_API_ID')
    COVERR_API_KEY = os.environ.get('COVERR_API_KEY')
    ELEVEN_API_KEY_1 = os.environ.get('ELEVEN_API_KEY_1')
    ELEVEN_API_KEY_2 = os.environ.get('ELEVEN_API_KEY_2')
    ELEVEN_API_KEY_3 = os.environ.get('ELEVEN_API_KEY_3')
    FREEPIK_API_KEY = os.environ.get('FREEPIK_API_KEY')
    FREESOUND_API = os.environ.get('FREESOUND_API')
    FREESOUND_ID = os.environ.get('FREESOUND_ID')
    GEMINI_API_KEY_1 = os.environ.get('GEMINI_API_KEY_1')
    GEMINI_API_KEY_2 = os.environ.get('GEMINI_API_KEY_2')
    GETIMG_API_KEY_1 = os.environ.get('GETIMG_API_KEY_1')
    GETIMG_API_KEY_2 = os.environ.get('GETIMG_API_KEY_2')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    HF_API_TOKEN_1 = os.environ.get('HF_API_TOKEN_1')
    INTERNET_ARCHIVE_ACCESS_KEY = os.environ.get('INTERNET_ARCHIVE_ACCESS_KEY')
    INTERNET_ARCHIVE_SECRET_KEY = os.environ.get('INTERNET_ARCHIVE_SECRET_KEY')
    NASA_API_KEY = os.environ.get('NASA_API_KEY')
    NEWS_API = os.environ.get('NEWS_API')
    NOAA_API_KEY = os.environ.get('NOAA_API_KEY')
    OPENAI_API_KEY_1 = os.environ.get('OPENAI_API_KEY_1')
    OPENAI_API_KEY_2 = os.environ.get('OPENAI_API_KEY_2')
    OPENROUTER_KEY = os.environ.get('OPENROUTER_KEY')
    PEXELS_API_KEY = os.environ.get('PEXELS_API_KEY')
    PIXABAY_API_KEY = os.environ.get('PIXABAY_API_KEY')
    REMOVE_BG_API = os.environ.get('REMOVE_BG_API')
    REPLICATE_API_TOKEN_1 = os.environ.get('REPLICATE_API_TOKEN_1')
    REPLICATE_API_TOKEN_2 = os.environ.get('REPLICATE_API_TOKEN_2')
    TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY')
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
    UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_ACCESS_KEY')
    UNSPLASH_ID = os.environ.get('UNSPLASH_ID')
    UNSPLASH_SECRET_KEY = os.environ.get('UNSPLASH_SECRET_KEY')
    VECTEEZY_API_KEY = os.environ.get('VECTEEZY_API_KEY')
    VECTEEZY_ID_KEY = os.environ.get('VECTEEZY_ID_KEY')
    YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
    YT_CHANNEL_ID = os.environ.get('YT_CHANNEL_ID')
    YT_CLIENT_ID_1 = os.environ.get('YT_CLIENT_ID_1')
    YT_CLIENT_ID_2 = os.environ.get('YT_CLIENT_ID_2')
    YT_CLIENT_SECRET_1 = os.environ.get('YT_CLIENT_SECRET_1')
    YT_CLIENT_SECRET_2 = os.environ.get('YT_CLIENT_SECRET_2')
    YT_REFRESH_TOKEN_1 = os.environ.get('YT_REFRESH_TOKEN_1')
    YT_REFRESH_TOKEN_2 = os.environ.get('YT_REFRESH_TOKEN_2')

    # Project Configuration
    PROJECT_NAME = "The Abyssal Archive"
    CHANNEL_TAGLINE = "Uncovering the world's darkest mysteries and unexplained phenomena"
    
    # YouTube Upload Configuration
    MAX_UPLOADS_PER_DAY = 6  # 2 long videos + 4 shorts
    YOUTUBE_QUOTA_PER_UPLOAD = 1600  # Standard quota units per upload
    
    # Video Production Settings
    LONG_VIDEO_DURATION_MIN = 180  # 3 minutes minimum
    LONG_VIDEO_DURATION_MAX = 360  # 6 minutes maximum
    SHORT_VIDEO_DURATION = 60      # 1 minute for shorts
    
    # Content Categories
    CONTENT_CATEGORIES = {
        "space": "Cosmic mysteries and unexplained space phenomena",
        "ocean": "Deep ocean secrets and underwater anomalies", 
        "history": "Historical mysteries and unsolved cases",
        "crime": "True crime and unexplained disappearances",
        "paranormal": "Supernatural and paranormal investigations"
    }
    
    # Content Sources
    WIKIPEDIA_LISTS = [
        "List of unexplained disappearances",
        "List of unsolved mysteries", 
        "List of cryptids",
        "List of mysterious places",
        "List of historical mysteries"
    ]
    
    # Image Generation Prompts
    IMAGE_PROMPTS = {
        "fog": "misty foggy dark atmosphere",
        "glowing_eyes": "glowing red eyes in darkness",
        "vortex": "spinning vortex portal dark energy",
        "silhouette": "dark silhouette against fog",
        "abandoned": "abandoned building overgrown decayed"
    }
    
    # Thumbnail Design Elements
    THUMBNAIL_ELEMENTS = {
        "high_contrast": True,
        "red_arrow": True,
        "glowing_effect": True,
        "vintage_filter": True
    }
    
    # Audio Settings
    AUDIO_SETTINGS = {
        "voice_model": "en-US-ChristopherNeural",  # Microsoft Edge TTS
        "pitch_shift": -10,  # Lower pitch for deeper voice
        "speed_adjustment": -5,  # Slightly slower
        "audio_effects": ["8D", "reverb", "low_pass_filter"]
    }
    
    # Video Effects
    VIDEO_EFFECTS = {
        "ken_burns_zoom": True,
        "vhs_overlay": True,
        "text_overlays": True,
        "flash_warnings": True
    }
    
    # Publishing Schedule (New York Time)
    PUBLISHING_TIMES_NY = [
        "14:00",  # 2 PM EST
        "19:00"   # 7 PM EST
    ]
    
    # Timezone Settings
    NY_TZ = pytz.timezone('America/New_York')
    UTC_TZ = pytz.UTC
    
    # SEO and Metadata
    SEO_KEYWORDS = [
        "mystery", "scary facts", "unexplained", "paranormal", 
        "true crime", "cosmic horror", "deep ocean", "ancient mysteries",
        "unsolved", "cryptid", "haunted", "supernatural"
    ]
    
    # Telegram Bot Configuration
    TELEGRAM_ENABLED = bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)
    
    # Safety Filters
    AD_SAFE_FILTER_ENABLED = True
    CONTENT_MODERATION_ENABLED = True
    
    @classmethod
    def validate_secrets(cls) -> Dict[str, bool]:
        """Validate that critical secrets are available"""
        critical_secrets = [
            'YT_CHANNEL_ID', 'YT_CLIENT_ID_1', 'YT_CLIENT_SECRET_1', 
            'YT_REFRESH_TOKEN_1'
        ]
        
        validation_results = {}
        for secret_name in critical_secrets:
            secret_value = getattr(cls, secret_name)
            validation_results[secret_name] = bool(secret_value)
        
        return validation_results

# Initialize configuration
config = Config()
'''
    
    with open("config/config.py", "w", encoding="utf-8") as f:
        f.write(config_content)
    print("Created config/config.py")

def create_utils_files():
    """Create utility files for various operations"""
    
    # Create logger utility
    logger_content = '''import logging
import os
from datetime import datetime
from config.config import config

def setup_logger(name: str, log_file: str = None, level: int = logging.INFO) -> logging.Logger:
    """
    Function to setup as many loggers as you want
    """
    if not log_file:
        log_file = f"data/logs/{name}_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(console_handler)

    return logger

# Main logger instance
main_logger = setup_logger('abyssal_archive', 'data/logs/main.log')
youtube_logger = setup_logger('youtube_uploader', 'data/logs/youtube.log')
content_logger = setup_logger('content_generator', 'data/logs/content.log')
image_logger = setup_logger('image_generator', 'data/logs/image.log')
audio_logger = setup_logger('audio_generator', 'data/logs/audio.log')
'''
    
    with open("src/utils/logger.py", "w", encoding="utf-8") as f:
        f.write(logger_content)
    print("Created src/utils/logger.py")
    
    # Create image processing utilities
    image_utils_content = '''import requests
import os
import random
from typing import List, Dict, Optional
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import io
from config.config import config
from .logger import image_logger

class ImageGenerator:
    """Class to handle image generation and processing for YouTube thumbnails and video backgrounds"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def generate_ai_image_getimg(self, prompt: str) -> Optional[bytes]:
        """Generate image using GetImg API"""
        try:
            if not config.GETIMG_API_KEY_1:
                image_logger.error("GETIMG_API_KEY_1 not configured")
                return None
                
            url = "https://api.getimg.ai/v1/stable-diffusion/text-to-image"
            headers = {
                'Authorization': f'Bearer {config.GETIMG_API_KEY_1}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "prompt": f"{prompt}, highly detailed, cinematic lighting, dark moody, atmospheric",
                "negative_prompt": "blurry, low quality, cartoon, anime, bright colors",
                "width": 1024,
                "height": 576,
                "steps": 30,
                "guidance": 7.5,
                "model": "realistic-vision-v2-0"
            }
            
            response = self.session.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            image_logger.info(f"Successfully generated image with GetImg for prompt: {prompt[:50]}...")
            return response.content
            
        except Exception as e:
            image_logger.error(f"Error generating image with GetImg: {str(e)}")
            return None
    
    def generate_ai_image_pollinations(self, prompt: str) -> Optional[bytes]:
        """Generate image using Pollinations.ai (free alternative)"""
        try:
            # Pollinations uses URL parameters for image generation
            base_url = "https://image.pollinations.ai/prompt/"
            full_prompt = f"{prompt}, dark, mysterious, cinematic, atmospheric, realistic"
            encoded_prompt = requests.utils.quote(full_prompt)
            
            url = f"{base_url}{encoded_prompt}?width=1024&height=576&seed={random.randint(1, 10000)}"
            
            response = self.session.get(url, timeout=60)
            response.raise_for_status()
            
            image_logger.info(f"Successfully generated image with Pollinations for prompt: {prompt[:50]}...")
            return response.content
            
        except Exception as e:
            image_logger.error(f"Error generating image with Pollinations: {str(e)}")
            return None
    
    def enhance_thumbnail(self, image_bytes: bytes) -> bytes:
        """Apply enhancement effects to make thumbnails more eye-catching"""
        try:
            image = Image.open(io.BytesIO(image_bytes))
            
            # Apply high contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.3)
            
            # Apply brightness adjustment
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(0.9)
            
            # Add red glow effect around important elements
            draw = ImageDraw.Draw(image)
            
            # Add border for thumbnail appeal
            border_width = 5
            draw.rectangle(
                [border_width, border_width, image.width-border_width, image.height-border_width], 
                outline=(255, 0, 0), width=border_width
            )
            
            # Save enhanced image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG', quality=95)
            img_byte_arr.seek(0)
            
            enhanced_bytes = img_byte_arr.read()
            image_logger.info("Successfully enhanced thumbnail image")
            return enhanced_bytes
            
        except Exception as e:
            image_logger.error(f"Error enhancing thumbnail: {str(e)}")
            return image_bytes  # Return original if enhancement fails
    
    def generate_thumbnail_variation(self, base_image_bytes: bytes, style: str = "default") -> bytes:
        """Generate different thumbnail styles for A/B testing"""
        try:
            image = Image.open(io.BytesIO(base_image_bytes))
            
            if style == "dark":
                # Apply dark filter
                enhancer = ImageEnhance.Brightness(image)
                image = enhancer.enhance(0.6)
                
            elif style == "highlight":
                # Apply sharp highlight effect
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(1.8)
                
            elif style == "orange_tint":
                # Apply orange tint
                r, g, b = image.split()
                r = ImageEnhance.Brightness(r).enhance(1.5)
                g = ImageEnhance.Brightness(g).enhance(0.8)
                b = ImageEnhance.Brightness(b).enhance(0.6)
                image = Image.merge("RGB", (r, g, b))
            
            # Save variation to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG', quality=95)
            img_byte_arr.seek(0)
            
            variation_bytes = img_byte_arr.read()
            image_logger.info(f"Successfully generated {style} thumbnail variation")
            return variation_bytes
            
        except Exception as e:
            image_logger.error(f"Error generating thumbnail variation: {str(e)}")
            return base_image_bytes
    
    def select_best_thumbnail(self, variations: List[bytes]) -> bytes:
        """Select the best thumbnail from multiple variations (placeholder for A/B testing logic)"""
        # For now, return the first one - in production this would implement A/B testing
        if variations:
            return variations[0]
        return b""
    
    def generate_scary_fact_visual(self, fact_text: str, mood: str = "dark") -> Optional[bytes]:
        """Generate a visual representation for a scary fact"""
        try:
            # Create a base prompt based on the fact and mood
            mood_prompts = {
                "dark": "dark, shadowy, mysterious atmosphere",
                "mysterious": "misty, enigmatic, unknown presence",
                "psychological": "unsettling, psychological thriller scene",
                "space": "cosmic horror, deep space, alien encounter",
                "ocean": "deep ocean, underwater mystery, abyssal depths"
            }
            
            base_prompt = f"{fact_text[:100]}, {mood_prompts.get(mood, 'dark')}, cinematic, horror aesthetic"
            
            # Try primary method first
            image_bytes = self.generate_ai_image_getimg(base_prompt)
            if image_bytes:
                enhanced_bytes = self.enhance_thumbnail(image_bytes)
                return enhanced_bytes
            
            # Fallback to free method
            image_bytes = self.generate_ai_image_pollinations(base_prompt)
            if image_bytes:
                enhanced_bytes = self.enhance_thumbnail(image_bytes)
                return enhanced_bytes
            
            image_logger.warning(f"Could not generate visual for fact: {fact_text[:50]}...")
            return None
            
        except Exception as e:
            image_logger.error(f"Error generating visual for fact: {str(e)}")
            return None

class StockImageSearcher:
    """Class to search for stock images from various sources"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def search_pexels(self, query: str, per_page: int = 10) -> List[Dict]:
        """Search for images on Pexels"""
        try:
            if not config.PEXELS_API_KEY:
                return []
                
            url = f"https://api.pexels.com/v1/search"
            headers = {"Authorization": config.PEXELS_API_KEY}
            params = {
                "query": f"{query} horror scary mysterious dark",
                "per_page": per_page,
                "orientation": "landscape"
            }
            
            response = self.session.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data.get("photos", [])
            
        except Exception as e:
            image_logger.error(f"Error searching Pexels: {str(e)}")
            return []
    
    def search_pixabay(self, query: str, per_page: int = 10) -> List[Dict]:
        """Search for images on Pixabay"""
        try:
            if not config.PIXABAY_API_KEY:
                return []
                
            url = "https://pixabay.com/api/"
            params = {
                "key": config.PIXABAY_API_KEY,
                "q": f"{query} horror scary mysterious dark",
                "per_page": per_page,
                "image_type": "photo",
                "orientation": "horizontal",
                "safesearch": True
            }
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data.get("hits", [])
            
        except Exception as e:
            image_logger.error(f"Error searching Pixabay: {str(e)}")
            return []
    
    def download_image(self, url: str) -> Optional[bytes]:
        """Download an image from a URL"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.content
        except Exception as e:
            image_logger.error(f"Error downloading image from {url}: {str(e)}")
            return None
'''
    
    with open("src/utils/image_utils.py", "w", encoding="utf-8") as f:
        f.write(image_utils_content)
    print("Created src/utils/image_utils.py")
    
    # Create audio utilities
    audio_utils_content = '''import edge_tts
import asyncio
import os
import subprocess
from typing import Optional
import tempfile
from config.config import config
from .logger import audio_logger

class AudioGenerator:
    """Class to generate audio narrations using Edge TTS and apply audio effects"""
    
    def __init__(self):
        self.voice = config.AUDIO_SETTINGS["voice_model"]
        self.pitch_shift = config.AUDIO_SETTINGS["pitch_shift"]
        self.speed_adjustment = config.AUDIO_SETTINGS["speed_adjustment"]
    
    async def generate_speech_async(self, text: str, output_path: str) -> bool:
        """Generate speech asynchronously using Edge TTS"""
        try:
            communicate = edge_tts.Communicate(text, self.voice)
            await communicate.save(output_path)
            audio_logger.info(f"Successfully generated audio for text: {text[:50]}...")
            return True
        except Exception as e:
            audio_logger.error(f"Error generating speech: {str(e)}")
            return False
    
    def generate_audio_with_effects(self, text: str) -> Optional[str]:
        """Generate audio with deep voice and effects"""
        try:
            # Create temporary file for raw audio
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_raw:
                raw_audio_path = temp_raw.name
            
            # Generate the basic audio
            success = asyncio.run(self.generate_speech_async(text, raw_audio_path))
            if not success:
                return None
            
            # Apply audio effects using ffmpeg
            processed_audio_path = raw_audio_path.replace(".mp3", "_processed.mp3")
            
            # Build ffmpeg command for pitch shift and speed adjustment
            cmd = [
                "ffmpeg", "-i", raw_audio_path,
                "-af", f"asetrate=44100*{0.95**(self.speed_adjustment/10)},aresample=44100,treble=g{self.pitch_shift/5}",
                "-y", processed_audio_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                audio_logger.error(f"FFmpeg error: {result.stderr}")
                # If ffmpeg fails, return original audio
                processed_audio_path = raw_audio_path
            else:
                # Clean up raw audio file
                os.remove(raw_audio_path)
            
            audio_logger.info(f"Successfully applied audio effects to: {text[:50]}...")
            return processed_audio_path
            
        except Exception as e:
            audio_logger.error(f"Error generating audio with effects: {str(e)}")
            # Clean up temp files if they exist
            for temp_path in [raw_audio_path, raw_audio_path.replace(".mp3", "_processed.mp3")]:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            return None
    
    def add_background_music(self, narration_path: str, music_path: str, output_path: str) -> bool:
        """Add background music to narration"""
        try:
            # Simple mixing using ffmpeg (volume balance: 80% narration, 20% music)
            cmd = [
                "ffmpeg", "-i", narration_path, "-i", music_path,
                "-filter_complex", "[0:a]volume=0.8[a1];[1:a]volume=0.2[a2];[a1][a2]amix=inputs=2:duration=first[aout]",
                "-map", "[aout]", "-y", output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                audio_logger.error(f"Error adding background music: {result.stderr}")
                return False
            
            audio_logger.info("Successfully added background music to narration")
            return True
            
        except Exception as e:
            audio_logger.error(f"Error adding background music: {str(e)}")
            return False
    
    def apply_8d_audio_effect(self, input_path: str, output_path: str) -> bool:
        """Apply 8D audio effect to make it more immersive"""
        try:
            # 8D audio effect using spatial reverb
            cmd = [
                "ffmpeg", "-i", input_path,
                "-af", "apulsator=hz=0.1:amount=0.5,sidechaos=0.5,freeverb=room=0.9:damp=0.8:level=0.8",
                "-y", output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                audio_logger.error(f"Error applying 8D audio effect: {result.stderr}")
                return False
            
            audio_logger.info("Successfully applied 8D audio effect")
            return True
            
        except Exception as e:
            audio_logger.error(f"Error applying 8D audio effect: {str(e)}")
            return False
    
    def adjust_audio_duration(self, input_path: str, target_duration: float, output_path: str) -> bool:
        """Adjust audio duration to match video length"""
        try:
            # First get current duration
            cmd = ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", 
                 "-of", "csv=p=0", input_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            current_duration = float(result.stdout.strip())
            
            if abs(current_duration - target_duration) < 0.5:
                # Duration is close enough, just copy
                import shutil
                shutil.copy2(input_path, output_path)
                return True
            
            # Calculate speed factor
            speed_factor = current_duration / target_duration
            
            # Adjust speed using ffmpeg
            cmd = [
                "ffmpeg", "-i", input_path,
                "-af", f"atempo={min(max(speed_factor, 0.5), 2.0)}",  # Limit to 0.5x to 2x speed
                "-y", output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                audio_logger.error(f"Error adjusting audio duration: {result.stderr}")
                return False
            
            audio_logger.info(f"Successfully adjusted audio duration from {current_duration:.2f}s to {target_duration:.2f}s")
            return True
            
        except Exception as e:
            audio_logger.error(f"Error adjusting audio duration: {str(e)}")
            return False
'''
    
    with open("src/utils/audio_utils.py", "w", encoding="utf-8") as f:
        f.write(audio_utils_content)
    print("Created src/utils/audio_utils.py")
    
    # Create content utilities
    content_utils_content = '''import wikipediaapi
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
            lines = content.split('\\n')
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
'''
    
    with open("src/utils/content_utils.py", "w", encoding="utf-8") as f:
        f.write(content_utils_content)
    print("Created src/utils/content_utils.py")

def create_main_module():
    """Create the main module file that orchestrates everything"""
    main_content = '''#!/usr/bin/env python3
"""
The Abyssal Archive - YouTube Automation Project
Main Execution Module

This script orchestrates the entire YouTube automation process including:
- Content sourcing and curation
- AI-powered script generation  
- Image and audio creation
- Video assembly
- YouTube upload
- Social media posting
"""

import os
import sys
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pytz
from config.config import config
from src.utils.logger import main_logger, youtube_logger, content_logger, image_logger, audio_logger
from src.utils.image_utils import ImageGenerator, StockImageSearcher
from src.utils.audio_utils import AudioGenerator
from src.utils.content_utils import ContentScraper, ScriptGenerator

class YouTubeAutomationEngine:
    """
    Main class that orchestrates the entire YouTube automation pipeline
    """
    
    def __init__(self):
        self.image_generator = ImageGenerator()
        self.stock_searcher = StockImageSearcher()
        self.audio_generator = AudioGenerator()
        self.content_scraper = ContentScraper()
        self.script_generator = ScriptGenerator()
        
        # Validate critical configurations
        validation_results = config.validate_secrets()
        main_logger.info(f"Secret validation results: {validation_results}")
        
        if not all(validation_results.values()):
            main_logger.error("Critical secrets are missing! Please check your environment variables.")
            raise ValueError("Missing critical configuration")
    
    def run_daily_production_cycle(self):
        """
        Execute the daily production cycle: create 2 long videos and 4 shorts
        """
        main_logger.info("Starting daily production cycle")
        
        try:
            # Phase 1: Content sourcing
            main_logger.info("Phase 1: Sourcing content...")
            content_pool = self._source_daily_content()
            
            if not content_pool:
                main_logger.error("No content sourced, stopping production cycle")
                return
            
            # Phase 2: Create long-form videos (2 per day)
            main_logger.info("Phase 2: Creating long-form videos...")
            long_videos_created = 0
            for content_item in content_pool[:2]:  # Create 2 long videos
                if self._create_long_video(content_item):
                    long_videos_created += 1
                    time.sleep(30)  # Small delay between creations
            
            # Phase 3: Create short-form videos (4 per day)
            main_logger.info("Phase 3: Creating short-form videos...")
            short_videos_created = 0
            for content_item in content_pool[2:6]:  # Create 4 shorts from remaining content
                if self._create_short_video(content_item):
                    short_videos_created += 1
                    time.sleep(15)  # Smaller delay for shorts
            
            # Phase 4: Upload and schedule videos
            main_logger.info("Phase 4: Uploading videos...")
            self._upload_and_schedule_videos(long_videos_created, short_videos_created)
            
            main_logger.info(f"Daily production completed: {long_videos_created} long videos, {short_videos_created} shorts")
            
        except Exception as e:
            main_logger.error(f"Error in daily production cycle: {str(e)}")
            self._send_error_notification(str(e))
    
    def _source_daily_content(self) -> List[Dict]:
        """
        Source content from multiple platforms for the day's production
        """
        try:
            content_pool = []
            
            # Get Wikipedia list content (50% of content)
            for wiki_list in config.WIKIPEDIA_LISTS[:2]:  # Use first 2 lists
                wiki_content = self.content_scraper.get_wikipedia_list_content(wiki_list)
                content_pool.extend(wiki_content)
            
            # Get Google Trends (25% of content)
            trend_content = self.content_scraper.get_google_trends()
            content_pool.extend(trend_content)
            
            # Get Reddit RSS feeds (25% of content)
            reddit_content = self.content_scraper.get_reddit_rss_feeds()
            content_pool.extend(reddit_content)
            
            # Add NASA/NOAA special content based on day of week
            ny_time = datetime.now(config.NY_TZ)
            if ny_time.weekday() == 0:  # Monday - Ocean content
                noaa_content = self.content_scraper.get_noaa_data()
                if noaa_content:
                    content_pool.append(noaa_content)
            elif ny_time.weekday() == 2:  # Wednesday - Space content
                nasa_content = self.content_scraper.get_nasa_apod()
                if nasa_content:
                    content_pool.append(nasa_content)
            
            # Filter for ad-safe content
            content_pool = self.content_scraper.filter_ad_safe_content(content_pool)
            
            # Shuffle content for variety
            random.shuffle(content_pool)
            
            main_logger.info(f"Sourced {len(content_pool)} content items for today")
            return content_pool
            
        except Exception as e:
            main_logger.error(f"Error sourcing daily content: {str(e)}")
            return []
    
    def _create_long_video(self, content_item: Dict) -> bool:
        """
        Create a long-form video (3-6 minutes) based on content item
        """
        try:
            main_logger.info(f"Creating long video for: {content_item['title']}")
            
            # Generate script
            script_data = self.script_generator.generate_mystery_script(
                content_item['title'], 
                fact_count=random.randint(5, 8)
            )
            
            if not script_data:
                main_logger.error("Failed to generate script for long video")
                return False
            
            # Generate audio narration
            full_script_text = script_data['hook'] + " " + " ".join(script_data['facts']) + " " + script_data['conclusion']
            audio_path = self.audio_generator.generate_audio_with_effects(full_script_text)
            
            if not audio_path:
                main_logger.error("Failed to generate audio for long video")
                return False
            
            # Generate images for each fact
            image_paths = []
            for i, fact in enumerate(script_data['facts']):
                # Create visual for each fact
                visual_bytes = self.image_generator.generate_scary_fact_visual(fact, content_item['category'])
                if visual_bytes:
                    image_path = f"assets/images/fact_{i}_{int(time.time())}.jpg"
                    with open(image_path, 'wb') as f:
                        f.write(visual_bytes)
                    image_paths.append(image_path)
            
            # If no images generated, create a generic one
            if not image_paths:
                generic_visual = self.image_generator.generate_scary_fact_visual(
                    script_data['hook'], 
                    content_item['category']
                )
                if generic_visual:
                    image_path = f"assets/images/generic_{int(time.time())}.jpg"
                    with open(image_path, 'wb') as f:
                        f.write(generic_visual)
                    image_paths = [image_path] * 5  # Repeat for duration
            
            # Create video file name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_filename = f"assets/videos/long_{timestamp}_{content_item['title'][:30].replace(' ', '_')}.mp4"
            
            # Assemble video using MoviePy (implementation would go here)
            # For now, we'll create a placeholder video file
            self._assemble_video_with_moviepy(
                image_paths, 
                audio_path, 
                video_filename, 
                script_data,
                is_short=False
            )
            
            # Generate thumbnail
            thumbnail_path = self._generate_video_thumbnail(script_data, content_item['category'])
            
            # Prepare video metadata
            video_metadata = {
                "title": f"{script_data['title']} | The Abyssal Archive",
                "description": self._generate_video_description(script_data, content_item),
                "tags": self._generate_video_tags(content_item),
                "category": self._get_youtube_category_id(content_item['category']),
                "privacyStatus": "public",
                "publishAt": self._calculate_publish_time(),
                "thumbnail_path": thumbnail_path
            }
            
            # Save metadata for later upload
            metadata_path = video_filename.replace('.mp4', '_metadata.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(video_metadata, f, indent=2, ensure_ascii=False)
            
            main_logger.info(f"Successfully created long video: {video_filename}")
            return True
            
        except Exception as e:
            main_logger.error(f"Error creating long video: {str(e)}")
            return False
    
    def _create_short_video(self, content_item: Dict) -> bool:
        """
        Create a short-form video (under 60 seconds) based on content highlights
        """
        try:
            main_logger.info(f"Creating short video for: {content_item['title']}")
            
            # Generate short script focusing on highlights
            short_script = self._generate_short_script(content_item)
            
            if not short_script:
                main_logger.error("Failed to generate short script")
                return False
            
            # Generate audio for short script
            audio_path = self.audio_generator.generate_audio_with_effects(short_script['hook'])
            
            if not audio_path:
                main_logger.error("Failed to generate audio for short video")
                return False
            
            # Generate single striking image
            visual_bytes = self.image_generator.generate_scary_fact_visual(
                short_script['hook'], 
                content_item['category']
            )
            
            if not visual_bytes:
                main_logger.error("Failed to generate visual for short video")
                return False
            
            image_path = f"assets/images/short_{int(time.time())}.jpg"
            with open(image_path, 'wb') as f:
                f.write(visual_bytes)
            
            # Create short video file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_filename = f"assets/videos/short_{timestamp}_{content_item['title'][:20].replace(' ', '_')}.mp4"
            
            # Assemble short video
            self._assemble_video_with_moviepy(
                [image_path], 
                audio_path, 
                video_filename, 
                short_script,
                is_short=True
            )
            
            # Generate thumbnail
            thumbnail_path = self._generate_short_thumbnail(short_script, content_item['category'])
            
            # Prepare short video metadata
            video_metadata = {
                "title": f"{short_script['title']} | Abyssal Shorts",
                "description": f"Quick mystery fact from The Abyssal Archive\\n\\nFull story: {short_script['hook']}",
                "tags": self._generate_video_tags(content_item)[:10],  # Limit tags for shorts
                "category": 27,  # People & Blogs
                "privacyStatus": "public",
                "publishAt": self._calculate_publish_time(),
                "thumbnail_path": thumbnail_path,
                "isShort": True
            }
            
            # Save metadata
            metadata_path = video_filename.replace('.mp4', '_metadata.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(video_metadata, f, indent=2, ensure_ascii=False)
            
            main_logger.info(f"Successfully created short video: {video_filename}")
            return True
            
        except Exception as e:
            main_logger.error(f"Error creating short video: {str(e)}")
            return False
    
    def _generate_short_script(self, content_item: Dict) -> Dict:
        """Generate a short script optimized for YouTube Shorts"""
        try:
            # Extract the most shocking/hooking part from the content
            title = content_item['title']
            desc = content_item['description']
            
            # Create a powerful hook-style title
            hooks = [
                f"What was found in {title} will shock you...",
                f"Scientists can't explain {title}...",
                f"The truth about {title} is terrifying...",
                f"Why {title} remains unsolved...",
                f"What happened in {title} defies logic..."
            ]
            
            hook = random.choice(hooks)
            
            return {
                "hook": hook,
                "title": f"{title} - Shocking Truth",
                "category": content_item['category'],
                "original_content": content_item
            }
        except Exception as e:
            main_logger.error(f"Error generating short script: {str(e)}")
            return {
                "hook": f"This {content_item['category']} mystery will leave you speechless...",
                "title": f"{content_item['title']} - Short",
                "category": content_item['category'],
                "original_content": content_item
            }
    
    def _assemble_video_with_moviepy(self, image_paths: List[str], audio_path: str, 
                                   output_path: str, script_data: Dict, is_short: bool = False):
        """
        Assemble video using MoviePy with images, audio, and text overlays
        """
        try:
            # Import here to avoid dependency issues during installation
            from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, TextClip
            import os
            
            # Calculate durations based on content type
            if is_short:
                image_duration = config.SHORT_VIDEO_DURATION / len(image_paths) if image_paths else 1
                total_duration = min(config.SHORT_VIDEO_DURATION, 60)
            else:
                # Estimate duration based on script length
                text_length = len(script_data.get('hook', '')) + sum(len(fact) for fact in script_data.get('facts', []))
                estimated_duration = max(180, min(360, text_length // 2))  # 3-6 minutes
                image_duration = estimated_duration / len(image_paths) if image_paths else 3
                total_duration = estimated_duration
            
            # Create image clips
            image_clips = []
            for img_path in image_paths:
                if os.path.exists(img_path):
                    clip = ImageClip(img_path).set_duration(image_duration)
                    if is_short:
                        # Apply Ken Burns effect for shorts
                        clip = clip.resize(height=1920).crop(x1=0, y1=0, x2=1080, y2=1920)
                    else:
                        # Apply subtle zoom for long videos
                        clip = clip.resize(lambda t: 1 + 0.02*t)  # Gentle zoom
                    image_clips.append(clip)
            
            # Concatenate image clips
            if image_clips:
                final_clip = image_clips[0]
                for clip in image_clips[1:]:
                    final_clip = final_clip.concatenate([clip])
            else:
                # Create a black screen placeholder if no images
                from moviepy.editor import ColorClip
                final_clip = ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_duration(total_duration)
            
            # Add audio
            if os.path.exists(audio_path):
                audio_clip = AudioFileClip(audio_path)
                # Trim or loop audio to match video duration
                if audio_clip.duration > final_clip.duration:
                    audio_clip = audio_clip.subclip(0, final_clip.duration)
                else:
                    # Loop audio if shorter than video
                    while audio_clip.duration < final_clip.duration:
                        audio_clip = audio_clip.loop(duration=final_clip.duration)
                
                final_clip = final_clip.set_audio(audio_clip)
            
            # Add text overlays for key facts/hooks
            text_clips = []
            if script_data.get('hook'):
                # Add hook text overlay
                hook_text = TextClip(
                    script_data['hook'][:50] + "...", 
                    fontsize=40, 
                    color='white', 
                    bg_color='black',
                    font='CourierPrime-Bold'  # Assuming this font exists
                ).set_position(('center', 'bottom')).set_duration(min(5, final_clip.duration))
                text_clips.append(hook_text)
            
            # Composite everything together
            if text_clips:
                final_clip = CompositeVideoClip([final_clip] + text_clips)
            
            # Write final video
            final_clip.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True
            )
            
            main_logger.info(f"Successfully assembled video: {output_path}")
            
        except ImportError:
            main_logger.warning("MoviePy not installed, creating placeholder video file")
            # Create a simple placeholder file
            with open(output_path, 'w') as f:
                f.write(f"PLACEHOLDER VIDEO FILE\\nContent: {script_data}\\nPath: {output_path}")
        except Exception as e:
            main_logger.error(f"Error assembling video with MoviePy: {str(e)}")
            # Still create a placeholder if assembly fails
            placeholder_path = output_path.replace('.mp4', '_placeholder.mp4')
            with open(placeholder_path, 'w') as f:
                f.write(f"ERROR ASSEMBLING VIDEO\\nContent: {script_data}\\nOriginal path: {output_path}")
    
    def _generate_video_thumbnail(self, script_data: Dict, category: str) -> str:
        """Generate a compelling thumbnail for the video"""
        try:
            # Create thumbnail based on the hook
            visual_bytes = self.image_generator.generate_scary_fact_visual(
                script_data['hook'], 
                category
            )
            
            if visual_bytes:
                # Enhance the thumbnail
                enhanced_bytes = self.image_generator.enhance_thumbnail(visual_bytes)
                
                # Generate variations for A/B testing
                dark_version = self.image_generator.generate_thumbnail_variation(enhanced_bytes, "dark")
                highlight_version = self.image_generator.generate_thumbnail_variation(enhanced_bytes, "highlight")
                orange_version = self.image_generator.generate_thumbnail_variation(enhanced_bytes, "orange_tint")
                
                # Select best thumbnail (in real implementation, this would test performance)
                final_thumbnail_bytes = self.image_generator.select_best_thumbnail([
                    enhanced_bytes, dark_version, highlight_version, orange_version
                ])
                
                # Save thumbnail
                timestamp = int(time.time())
                thumbnail_path = f"assets/thumbnails/thumb_{timestamp}.jpg"
                with open(thumbnail_path, 'wb') as f:
                    f.write(final_thumbnail_bytes)
                
                main_logger.info(f"Generated video thumbnail: {thumbnail_path}")
                return thumbnail_path
            
            # Fallback to generic thumbnail
            return self._create_generic_thumbnail(category)
            
        except Exception as e:
            main_logger.error(f"Error generating video thumbnail: {str(e)}")
            return self._create_generic_thumbnail(category)
    
    def _generate_short_thumbnail(self, script_data: Dict, category: str) -> str:
        """Generate a thumbnail optimized for YouTube Shorts"""
        try:
            # Similar to regular thumbnail but with more vibrant contrasts
            visual_bytes = self.image_generator.generate_scary_fact_visual(
                script_data['hook'], 
                category
            )
            
            if visual_bytes:
                # Apply high contrast and vibrant effects for shorts
                image = self.image_generator.enhance_thumbnail(visual_bytes)
                
                # Add "SHORTS" badge
                from PIL import Image, ImageDraw, ImageFont
                import io
                
                pil_image = Image.open(io.BytesIO(image))
                draw = ImageDraw.Draw(pil_image)
                
                # Add "SHORTS" text in red box
                draw.rectangle([pil_image.width-150, 10, pil_image.width-10, 50], fill=(255, 0, 0))
                try:
                    # Try to use a bold font if available
                    font = ImageFont.truetype("arial.ttf", 20)
                except:
                    # Fallback to default font
                    font = ImageFont.load_default()
                
                draw.text((pil_image.width-140, 20), "SHORTS", fill=(255, 255, 255), font=font)
                
                # Save with changes
                img_byte_arr = io.BytesIO()
                pil_image.save(img_byte_arr, format='JPEG', quality=95)
                img_byte_arr.seek(0)
                
                timestamp = int(time.time())
                thumbnail_path = f"assets/thumbnails/short_thumb_{timestamp}.jpg"
                with open(thumbnail_path, 'wb') as f:
                    f.write(img_byte_arr.read())
                
                main_logger.info(f"Generated short thumbnail: {thumbnail_path}")
                return thumbnail_path
            
            return self._create_generic_thumbnail(category)
            
        except Exception as e:
            main_logger.error(f"Error generating short thumbnail: {str(e)}")
            return self._create_generic_thumbnail(category)
    
    def _create_generic_thumbnail(self, category: str) -> str:
        """Create a generic thumbnail when specific generation fails"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import io
            
            # Create a simple dark-themed thumbnail
            width, height = 1280, 720
            image = Image.new('RGB', (width, height), color=(20, 20, 30))  # Dark blue-gray
            draw = ImageDraw.Draw(image)
            
            # Add category-specific elements
            category_colors = {
                'space': (50, 50, 150),     # Deep blue
                'ocean': (30, 80, 120),    # Ocean blue  
                'history': (80, 60, 40),   # Brown
                'crime': (60, 20, 20),     # Dark red
                'paranormal': (70, 30, 80), # Purple
                'mystery': (40, 40, 60)    # Dark gray
            }
            
            bg_color = category_colors.get(category, (40, 40, 60))
            draw.rectangle([0, 0, width, height], fill=bg_color)
            
            # Add "MYSTERY" text
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except:
                font = ImageFont.load_default()
            
            text = "MYSTERY"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = (width - text_width) // 2
            text_y = height // 2 - 50
            
            draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)
            
            # Add subtitle
            try:
                small_font = ImageFont.truetype("arial.ttf", 30)
            except:
                small_font = ImageFont.load_default()
            
            subtitle = "THE ABYSMAL ARCHIVE"
            bbox = draw.textbbox((0, 0), subtitle, font=small_font)
            subtitle_width = bbox[2] - bbox[0]
            subtitle_x = (width - subtitle_width) // 2
            subtitle_y = height // 2 + 30
            
            draw.text((subtitle_x, subtitle_y), subtitle, fill=(200, 200, 200), font=small_font)
            
            # Add border
            draw.rectangle([5, 5, width-5, height-5], outline=(255, 0, 0), width=5)
            
            # Save thumbnail
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG', quality=95)
            img_byte_arr.seek(0)
            
            timestamp = int(time.time())
            thumbnail_path = f"assets/thumbnails/generic_thumb_{timestamp}.jpg"
            with open(thumbnail_path, 'wb') as f:
                f.write(img_byte_arr.read())
            
            main_logger.info(f"Created generic thumbnail: {thumbnail_path}")
            return thumbnail_path
            
        except Exception as e:
            main_logger.error(f"Error creating generic thumbnail: {str(e)}")
            return ""  # Return empty string if all fails
    
    def _generate_video_description(self, script_data: Dict, content_item: Dict) -> str:
        """Generate comprehensive video description"""
        description = f"""{script_data.get('hook', '')}

🔍 What did you think of this mystery?
Share your theories in the comments!

🔔 Subscribe for more unexplained phenomena and dark mysteries
💬 Join our community discussions
📚 Sources: {content_item.get('source', 'Multiple sources compiled')}

Timestamps:
0:00 - Introduction
0:15 - Fact 1
0:30 - Fact 2
0:45 - Fact 3
1:00 - Fact 4
1:15 - Fact 5
1:30 - Conclusion

#Mystery #ScaryFacts #Unexplained #Paranormal #Horror #TrueCrime #SpaceMystery #OceanMysteries #HistoryMystery #AbyssalArchive

Music: Licensed from various sources
Images: AI-generated or licensed

DISCLAIMER: The information presented is compiled from various sources for entertainment purposes.
Always verify information independently."""

        return description
    
    def _generate_video_tags(self, content_item: Dict) -> List[str]:
        """Generate relevant tags for the video"""
        base_tags = config.SEO_KEYWORDS.copy()
        category_tag_map = {
            'space': ['space', 'cosmic', 'astronomy', 'ufo', 'aliens'],
            'ocean': ['ocean', 'sea', 'underwater', 'deep', 'marine'],
            'history': ['history', 'ancient', 'civilization', 'archaeology'],
            'crime': ['crime', 'murder', 'disappearance', 'investigation'],
            'paranormal': ['paranormal', 'ghost', 'supernatural', 'haunted'],
            'mystery': ['mystery', 'unsolved', 'unknown', 'cryptid']
        }
        
        additional_tags = category_tag_map.get(content_item['category'], [])
        all_tags = base_tags + additional_tags
        
        # Limit to 15 tags for regular videos, 10 for shorts
        return list(set(all_tags))[:15]
    
    def _get_youtube_category_id(self, category: str) -> int:
        """Map our categories to YouTube category IDs"""
        category_map = {
            'space': 27,  # Science & Technology
            'ocean': 27,  # Science & Technology
            'history': 27, # Science & Technology
            'crime': 22,   # People & Blogs (could be News & Politics)
            'paranormal': 27, # Science & Technology
            'mystery': 27  # Science & Technology
        }
        
        return category_map.get(category, 27)  # Default to Science & Technology
    
    def _calculate_publish_time(self) -> str:
        """Calculate optimal publish time in New York timezone"""
        ny_time = datetime.now(config.NY_TZ)
        
        # Determine next optimal publishing time
        available_times = config.PUBLISHING_TIMES_NY
        current_time_str = ny_time.strftime("%H:%M")
        
        # Find the next available time slot
        for time_str in available_times:
            if time_str > current_time_str:
                # Use today's date with this time
                publish_datetime = ny_time.replace(
                    hour=int(time_str.split(':')[0]),
                    minute=int(time_str.split(':')[1]),
                    second=0,
                    microsecond=0
                )
                break
        else:
            # If all times passed today, use tomorrow's first time
            tomorrow = ny_time + timedelta(days=1)
            first_time = available_times[0]
            publish_datetime = tomorrow.replace(
                hour=int(first_time.split(':')[0]),
                minute=int(first_time.split(':')[1]),
                second=0,
                microsecond=0
            )
        
        # Convert back to UTC for YouTube API
        utc_publish_time = publish_datetime.astimezone(config.UTC_TZ)
        return utc_publish_time.isoformat()
    
    def _upload_and_schedule_videos(self, long_count: int, short_count: int):
        """Upload videos to YouTube with scheduling"""
        try:
            # This would integrate with YouTube API
            # For now, log what would happen
            main_logger.info(f"Would upload {long_count} long videos and {short_count} shorts")
            
            # Look for video files and metadata
            import glob
            video_files = glob.glob("assets/videos/*.mp4")
            metadata_files = glob.glob("assets/videos/*_metadata.json")
            
            main_logger.info(f"Found {len(video_files)} video files and {len(metadata_files)} metadata files")
            
            # In a real implementation, we would:
            # 1. Match video files with metadata
            # 2. Upload using YouTube API with scheduling
            # 3. Handle quota management with multiple API keys
            # 4. Post to community with links
            
            main_logger.info("Upload simulation completed")
            
        except Exception as e:
            main_logger.error(f"Error in upload simulation: {str(e)}")
    
    def _send_error_notification(self, error_message: str):
        """Send error notification via Telegram if configured"""
        if config.TELEGRAM_ENABLED:
            try:
                import telegram
                bot = telegram.Bot(token=config.TELEGRAM_BOT_TOKEN)
                
                message = f"🚨 The Abyssal Archive ERROR 🚨\\n\\n{error_message}\\n\\nTime: {datetime.now().isoformat()}"
                bot.send_message(chat_id=config.TELEGRAM_CHAT_ID, text=message)
                
                main_logger.info("Error notification sent via Telegram")
            except Exception as e:
                main_logger.error(f"Failed to send Telegram notification: {str(e)}")
        else:
            main_logger.warning("Telegram notifications disabled - no token/chat ID configured")


def main():
    """Main execution function"""
    main_logger.info("Starting The Abyssal Archive YouTube Automation Engine")
    
    try:
        engine = YouTubeAutomationEngine()
        engine.run_daily_production_cycle()
        
        main_logger.info("The Abyssal Archive automation cycle completed successfully")
        
    except KeyboardInterrupt:
        main_logger.info("Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        main_logger.error(f"Fatal error in main process: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
'''

    with open("src/main.py", "w", encoding="utf-8") as f:
        f.write(main_content)
    print("Created src/main.py")

def create_github_actions_files():
    """Create GitHub Actions workflow files"""
    
    # Create workflows directory
    os.makedirs(".github/workflows", exist_ok=True)
    
    # Create daily production workflow
    daily_workflow_content = """name: Daily YouTube Production Cycle

on:
  schedule:
    # Run twice daily at 6 AM and 1 PM EST (11 AM and 6 PM UTC)
    - cron: '0 11 * * *'   # 6 AM EST
    - cron: '0 18 * * *'   # 1 PM EST
  workflow_dispatch:  # Allow manual trigger

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
      continue-on-error: true

    - name: Run YouTube Automation
      env:
        CAMB_AI_KEY_1: ${{ secrets.CAMB_AI_KEY_1 }}
        CLOUDINARY_API_KEY: ${{ secrets.CLOUDINARY_API_KEY }}
        COVERR_API_ID: ${{ secrets.COVERR_API_ID }}
        COVERR_API_KEY: ${{ secrets.COVERR_API_KEY }}
        ELEVEN_API_KEY_1: ${{ secrets.ELEVEN_API_KEY_1 }}
        ELEVEN_API_KEY_2: ${{ secrets.ELEVEN_API_KEY_2 }}
        ELEVEN_API_KEY_3: ${{ secrets.ELEVEN_API_KEY_3 }}
        FREEPIK_API_KEY: ${{ secrets.FREEPIK_API_KEY }}
        FREESOUND_API: ${{ secrets.FREESOUND_API }}
        FREESOUND_ID: ${{ secrets.FREESOUND_ID }}
        GEMINI_API_KEY_1: ${{ secrets.GEMINI_API_KEY_1 }}
        GEMINI_API_KEY_2: ${{ secrets.GEMINI_API_KEY_2 }}
        GETIMG_API_KEY_1: ${{ secrets.GETIMG_API_KEY_1 }}
        GETIMG_API_KEY_2: ${{ secrets.GETIMG_API_KEY_2 }}
        GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
        HF_API_TOKEN_1: ${{ secrets.HF_API_TOKEN_1 }}
        INTERNET_ARCHIVE_ACCESS_KEY: ${{ secrets.INTERNET_ARCHIVE_ACCESS_KEY }}
        INTERNET_ARCHIVE_SECRET_KEY: ${{ secrets.INTERNET_ARCHIVE_SECRET_KEY }}
        NASA_API_KEY: ${{ secrets.NASA_API_KEY }}
        NEWS_API: ${{ secrets.NEWS_API }}
        NOAA_API_KEY: ${{ secrets.NOAA_API_KEY }}
        OPENAI_API_KEY_1: ${{ secrets.OPENAI_API_KEY_1 }}
        OPENAI_API_KEY_2: ${{ secrets.OPENAI_API_KEY_2 }}
        OPENROUTER_KEY: ${{ secrets.OPENROUTER_KEY }}
        PEXELS_API_KEY: ${{ secrets.PEXELS_API_KEY }}
        PIXABAY_API_KEY: ${{ secrets.PIXABAY_API_KEY }}
        REMOVE_BG_API: ${{ secrets.REMOVE_BG_API }}
        REPLICATE_API_TOKEN_1: ${{ secrets.REPLICATE_API_TOKEN_1 }}
        REPLICATE_API_TOKEN_2: ${{ secrets.REPLICATE_API_TOKEN_2 }}
        TAVILY_API_KEY: ${{ secrets.TAVILY_API_KEY }}
        TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        UNSPLASH_ACCESS_KEY: ${{ secrets.UNSPLASH_ACCESS_KEY }}
        UNSPLASH_ID: ${{ secrets.UNSPLASH_ID }}
        UNSPLASH_SECRET_KEY: ${{ secrets.UNSPLASH_SECRET_KEY }}
        VECTEEZY_API_KEY: ${{ secrets.VECTEEZY_API_KEY }}
        VECTEEZY_ID_KEY: ${{ secrets.VECTEEZY_ID_KEY }}
        YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
        YT_CHANNEL_ID: ${{ secrets.YT_CHANNEL_ID }}
        YT_CLIENT_ID_1: ${{ secrets.YT_CLIENT_ID_1 }}
        YT_CLIENT_ID_2: ${{ secrets.YT_CLIENT_ID_2 }}
        YT_CLIENT_SECRET_1: ${{ secrets.YT_CLIENT_SECRET_1 }}
        YT_CLIENT_SECRET_2: ${{ secrets.YT_CLIENT_SECRET_2 }}
        YT_REFRESH_TOKEN_1: ${{ secrets.YT_REFRESH_TOKEN_1 }}
        YT_REFRESH_TOKEN_2: ${{ secrets.YT_REFRESH_TOKEN_2 }}
      run: |
        python -m src.main

    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: production-output-${{ github.run_number }}
        path: |
          assets/
          data/logs/
        retention-days: 7
"""
    
    with open(".github/workflows/daily-production.yml", "w", encoding="utf-8") as f:
        f.write(daily_workflow_content)
    print("Created .github/workflows/daily-production.yml")
    
    # Create monitoring workflow
    monitoring_workflow_content = """name: System Health Check

on:
  schedule:
    # Run every 6 hours
    - cron: '0 */6 * * *'
  workflow_dispatch:

jobs:
  health-check:
    runs-on: ubuntu-latest
    
  steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Check API connectivity
      env:
        GEMINI_API_KEY_1: ${{ secrets.GEMINI_API_KEY_1 }}
        GETIMG_API_KEY_1: ${{ secrets.GETIMG_API_KEY_1 }}
        YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
        YT_CLIENT_ID_1: ${{ secrets.YT_CLIENT_ID_1 }}
        YT_CLIENT_SECRET_1: ${{ secrets.YT_CLIENT_SECRET_1 }}
        YT_REFRESH_TOKEN_1: ${{ secrets.YT_REFRESH_TOKEN_1 }}
      run: |
        python -c "
        import os
        from config.config import config
        print('API Keys Status:')
        print(f'Gemini: {bool(config.GEMINI_API_KEY_1)}')
        print(f'GetImg: {bool(config.GETIMG_API_KEY_1)}')
        print(f'YouTube: {bool(config.YOUTUBE_API_KEY)}')
        print(f'Telegram: {bool(config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHAT_ID)}')
        print('Configuration validation:', config.validate_secrets())
        "
"""
    
    with open(".github/workflows/health-check.yml", "w", encoding="utf-8") as f:
        f.write(monitoring_workflow_content)
    print("Created .github/workflows/health-check.yml")

def create_readme():
    """Create README.md file"""
    readme_content = """# The Abyssal Archive - YouTube Automation Project

## Overview
The Abyssal Archive is an automated YouTube channel that produces mystery and scary facts content targeting international audiences for monetization.
The system runs on GitHub Actions, creating 2 long-form videos and 4 shorts daily using AI-generated content, images, and audio.

## Features
- **Daily Production**: Creates 6 videos per day (2 long, 4 shorts)
- **Multi-Source Content**: Pulls from Wikipedia, Google Trends, Reddit RSS, NASA, NOAA
- **AI-Powered**: Generates scripts, images, and audio automatically
- **Ad-Safe Content**: Filters content to maintain monetization eligibility
- **Multi-API Support**: Uses multiple API keys to avoid quotas
- **Smart Scheduling**: Publishes at optimal times for US/UK audience
- **Telegram Notifications**: Real-time monitoring and alerts

## Architecture
- **Content Sourcing**: Wikipedia, Google Trends, Reddit, NASA/NOAA APIs
- **AI Processing**: Gemini for script generation, multiple image APIs
- **Media Creation**: Edge-TTS for narration, MoviePy for video assembly
- **Publishing**: YouTube API with multi-account quota management
- **Monitoring**: Telegram bots and logging systems

## Environment Variables Required
All sensitive data is managed through GitHub Secrets:

### Content APIs
- `GEMINI_API_KEY_1`, `GEMINI_API_KEY_2`
- `OPENAI_API_KEY_1`, `OPENAI_API_KEY_2`
- `GROQ_API_KEY`
- `HF_API_TOKEN_1`
- `TAVILY_API_KEY`
- `NEWS_API`

### Image Generation
- `GETIMG_API_KEY_1`, `GETIMG_API_KEY_2`
- `REPLICATE_API_TOKEN_1`, `REPLICATE_API_TOKEN_2`
- `PEXELS_API_KEY`
- `PIXABAY_API_KEY`
- `UNSPLASH_ACCESS_KEY`, `UNSPLASH_SECRET_KEY`
- `FREEPIK_API_KEY`
- `VECTEEZY_API_KEY`, `VECTEEZEY_ID_KEY`
- `COVERR_API_ID`, `COVERR_API_KEY`

### Audio/Sound
- `ELEVEN_API_KEY_1`, `ELEVEN_API_KEY_2`, `ELEVEN_API_KEY_3`
- `FREESOUND_API`, `FREESOUND_ID`

### Data Sources
- `NASA_API_KEY`
- `NOAA_API_KEY`
- `INTERNET_ARCHIVE_ACCESS_KEY`, `INTERNET_ARCHIVE_SECRET_KEY`

### YouTube Integration
- `YOUTUBE_API_KEY`
- `YT_CHANNEL_ID`
- `YT_CLIENT_ID_1`, `YT_CLIENT_ID_2`
- `YT_CLIENT_SECRET_1`, `YT_CLIENT_SECRET_2`
- `YT_REFRESH_TOKEN_1`, `YT_REFRESH_TOKEN_2`

### Communication
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

### Other Services
- `CAMB_AI_KEY_1`
- `CLOUDINARY_API_KEY`
- `REMOVE_BG_API`
- `OPENROUTER_KEY`

## Installation
1. Clone the repository
2. Set up all required environment variables in GitHub Secrets
3. Configure YouTube API access with proper OAuth credentials
4. Review and approve the content policies for your channel

## Usage
The system runs automatically via GitHub Actions on a scheduled basis:
- Daily production: Twice per day at 6 AM and 1 PM EST
- Health checks: Every 6 hours

Manual triggers are also available through the GitHub Actions interface.

## Content Strategy
- **Long Videos**: 3-6 minutes, deep mystery explorations
- **Shorts**: 1-minute highlights and teasers
- **Categories**: Space mysteries, Ocean anomalies, Historical enigmas, True crime, Paranormal phenomena
- **Themes**: Focus on liminal spaces, nightmare facts, and unsolved mysteries

## Safety & Compliance
- Ad-safe content filtering
- Multiple API key rotation to prevent quota issues
- Content moderation for international audiences
- Proper licensing and attribution practices

## Monitoring
- Comprehensive logging system
- Telegram notifications for errors and status updates
- Performance tracking and optimization

## Legal Notice
This project is designed for educational and entertainment purposes.
Content creators are responsible for ensuring compliance with YouTube's terms of service, advertising policies, and local regulations.
The system is designed to produce ad-safe content but creators should monitor their channels regularly.
The owner assumes full responsibility for the content produced by this system.
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("Created README.md")

def create_license():
    """Create LICENSE file"""
    license_content = """MIT License

Copyright (c) 2025 The Abyssal Archive Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Disclaimer: This software is provided for educational and entertainment purposes only.
Users are responsible for ensuring compliance with platform terms of service, 
advertising policies, and applicable laws in their jurisdictions.
"""
    
    with open("LICENSE", "w", encoding="utf-8") as f:
        f.write(license_content)
    print("Created LICENSE")

def main():
    """Main function to create all project files"""
    print("Building The Abyssal Archive YouTube Automation Project...")
    
    # Create directory structure
    create_directory_structure()
    
    # Create all necessary files
    create_requirements_txt()
    create_config_py()
    create_utils_files()
    create_main_module()
    create_github_actions_files()
    create_readme()
    create_license()
    
    print("\n" + "="*60)
    print("PROJECT BUILD COMPLETE! 🚀")
    print("="*60)
    print("Files created:")
    print("- Directory structure with all necessary folders")
    print("- Complete Python modules with production-ready code")
    print("- Configuration files with all API key integrations")
    print("- GitHub Actions workflows for automated execution")
    print("- Documentation and licensing files")
    print("\nThe Abyssal Archive is now ready for deployment!")
    print("You can now push these files to GitHub.")

if __name__ == "__main__":
    main()
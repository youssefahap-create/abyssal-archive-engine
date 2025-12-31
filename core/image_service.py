import os
import random
import requests
from pathlib import Path
from typing import Optional, Tuple, List
from PIL import Image, ImageFilter
import io

from config import config
from core.logger import logger

class ImageService:
    def __init__(self):
        self.pexels_key = os.getenv("PEXELS_API_KEY")
        self.unsplash_access = os.getenv("UNSPLASH_ACCESS_KEY")
        self.pixabay_key = os.getenv("PIXABAY_API_KEY")
        self.freepik_key = os.getenv("FREEPIK_API_KEY")
        self.vecteezy_key = os.getenv("VECTEEZY_API_KEY")
        
        # Local image cache
        self.local_images = self._load_local_images()
    
    def _load_local_images(self) -> List[Path]:
        """Load local images from assets directory"""
        local_dir = config.ASSETS_DIR / "backgrounds"
        local_dir.mkdir(parents=True, exist_ok=True)
        
        images = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.webp']:
            images.extend(list(local_dir.glob(ext)))
        
        return images
    
    def get_question_image(self, question_type: str, search_query: str = None) -> Optional[Path]:
        """Get image for question with fallback providers"""
        
        if not search_query:
            search_query = self._generate_search_query(question_type)
        
        for provider in config.IMAGE_PROVIDERS:
            try:
                if provider == "pexels" and self.pexels_key:
                    image_path = self._pexels_image(search_query)
                    if image_path:
                        return image_path
                
                elif provider == "unsplash" and self.unsplash_access:
                    image_path = self._unsplash_image(search_query)
                    if image_path:
                        return image_path
                
                elif provider == "pixabay" and self.pixabay_key:
                    image_path = self._pixabay_image(search_query)
                    if image_path:
                        return image_path
                
                elif provider == "freepik" and self.freepik_key:
                    image_path = self._freepik_image(search_query)
                    if image_path:
                        return image_path
                
                elif provider == "vecteezy" and self.vecteezy_key:
                    image_path = self._vecteezy_image(search_query)
                    if image_path:
                        return image_path
                
                elif provider == "local":
                    image_path = self._local_image(search_query)
                    if image_path:
                        return image_path
                        
            except Exception as e:
                logger.warning(f"Image provider {provider} failed: {str(e)}")
                continue
        
        # If all fail, create a colored background
        return self._create_color_background()
    
    def _generate_search_query(self, question_type: str) -> str:
        """Generate search query based on question type"""
        queries = {
            "flag": ["country flag", "national flag", "flags of the world"],
            "landmark": ["famous landmarks", "world monuments", "tourist attractions"],
            "animal": ["wild animals", "nature photography", "animal closeup"],
            "science": ["science concepts", "laboratory equipment", "scientific phenomena"],
            "history": ["historical events", "ancient artifacts", "historical figures"],
            "art": ["famous paintings", "art masterpieces", "classical art"],
            "food": ["world cuisine", "delicious food", "gourmet dishes"],
            "sports": ["sports equipment", "athletes in action", "sports moments"]
        }
        
        return random.choice(queries.get(question_type, ["abstract background", "colorful pattern"]))
    
    def _pexels_image(self, query: str) -> Optional[Path]:
        """Get image from Pexels"""
        try:
            url = "https://api.pexels.com/v1/search"
            headers = {"Authorization": self.pexels_key}
            params = {
                "query": query,
                "per_page": 10,
                "orientation": "portrait"
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data.get("photos"):
                photo = random.choice(data["photos"])
                image_url = photo["src"]["large"]
                
                return self._download_image(image_url, "pexels")
            
        except Exception as e:
            logger.error(f"Pexels API failed: {str(e)}")
        
        return None
    
    def _unsplash_image(self, query: str) -> Optional[Path]:
        """Get image from Unsplash"""
        try:
            url = "https://api.unsplash.com/photos/random"
            headers = {"Authorization": f"Client-ID {self.unsplash_access}"}
            params = {
                "query": query,
                "orientation": "portrait",
                "count": 10
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                photo = random.choice(data)
                image_url = photo["urls"]["regular"]
                
                return self._download_image(image_url, "unsplash")
            
        except Exception as e:
            logger.error(f"Unsplash API failed: {str(e)}")
        
        return None
    
    def _pixabay_image(self, query: str) -> Optional[Path]:
        """Get image from Pixabay"""
        try:
            url = "https://pixabay.com/api/"
            params = {
                "key": self.pixabay_key,
                "q": query,
                "image_type": "photo",
                "orientation": "vertical",
                "per_page": 20
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data.get("hits"):
                hit = random.choice(data["hits"])
                image_url = hit["largeImageURL"]
                
                return self._download_image(image_url, "pixabay")
            
        except Exception as e:
            logger.error(f"Pixabay API failed: {str(e)}")
        
        return None
    
    def _freepik_image(self, query: str) -> Optional[Path]:
        """Get image from Freepik"""
        try:
            url = "https://api.freepik.com/v1/resources"
            headers = {"X-Freepik-API-Key": self.freepik_key}
            params = {
                "query": query,
                "locale": "en-US",
                "limit": 20,
                "order": "latest"
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data.get("data"):
                item = random.choice(data["data"])
                image_url = item["image"]["source"]
                
                return self._download_image(image_url, "freepik")
            
        except Exception as e:
            logger.error(f"Freepik API failed: {str(e)}")
        
        return None
    
    def _vecteezy_image(self, query: str) -> Optional[Path]:
        """Get image from Vecteezy"""
        try:
            url = "https://api.vecteezy.com/v2/public/search"
            headers = {"X-API-KEY": self.vecteezy_key}
            params = {
                "query": query,
                "page": 1,
                "per_page": 20,
                "media_type": "photo"
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data.get("data"):
                item = random.choice(data["data"])
                image_url = item["attributes"]["image_url"]
                
                return self._download_image(image_url, "vecteezy")
            
        except Exception as e:
            logger.error(f"Vecteezy API failed: {str(e)}")
        
        return None
    
    def _local_image(self, query: str) -> Optional[Path]:
        """Get local image"""
        if not self.local_images:
            return None
        
        # Try to find image matching query
        matching_images = []
        for img_path in self.local_images:
            if query.lower() in img_path.name.lower():
                matching_images.append(img_path)
        
        if matching_images:
            selected = random.choice(matching_images)
        else:
            selected = random.choice(self.local_images)
        
        # Apply blur effect
        return self._apply_blur_effect(selected)
    
    def _create_color_background(self) -> Path:
        """Create a solid color background"""
        try:
            image_dir = config.STORAGE_DIR / "images" / config.today_str
            image_dir.mkdir(parents=True, exist_ok=True)
            
            image_path = image_dir / f"background_{config.timestamp_str}.png"
            
            # Create gradient background
            from PIL import ImageDraw
            
            img = Image.new('RGB', (config.VIDEO_WIDTH, config.VIDEO_HEIGHT), config.BACKGROUND_COLOR)
            draw = ImageDraw.Draw(img)
            
            # Add subtle gradient
            for i in range(config.VIDEO_HEIGHT):
                alpha = i / config.VIDEO_HEIGHT
                r = int(int(config.BACKGROUND_COLOR[1:3], 16) * (1 - alpha) + int(config.SECONDARY_COLOR[1:3], 16) * alpha)
                g = int(int(config.BACKGROUND_COLOR[3:5], 16) * (1 - alpha) + int(config.SECONDARY_COLOR[3:5], 16) * alpha)
                b = int(int(config.BACKGROUND_COLOR[5:7], 16) * (1 - alpha) + int(config.SECONDARY_COLOR[5:7], 16) * alpha)
                color = f"#{r:02x}{g:02x}{b:02x}"
                draw.line([(0, i), (config.VIDEO_WIDTH, i)], fill=color)
            
            # Apply blur
            img = img.filter(ImageFilter.GaussianBlur(radius=10))
            
            img.save(image_path)
            
            return image_path
            
        except Exception as e:
            logger.error(f"Failed to create background: {str(e)}")
            return None
    
    def _download_image(self, url: str, source: str) -> Optional[Path]:
        """Download and save image"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            image_dir = config.STORAGE_DIR / "images" / config.today_str
            image_dir.mkdir(parents=True, exist_ok=True)
            
            image_path = image_dir / f"{source}_{config.timestamp_str}.jpg"
            
            with open(image_path, "wb") as f:
                f.write(response.content)
            
            # Apply blur effect
            blurred_path = self._apply_blur_effect(image_path)
            
            return blurred_path
            
        except Exception as e:
            logger.error(f"Failed to download image from {source}: {str(e)}")
            return None
    
    def _apply_blur_effect(self, image_path: Path) -> Path:
        """Apply strong blur effect to image"""
        try:
            with Image.open(image_path) as img:
                # Resize to video dimensions
                img = img.resize((config.VIDEO_WIDTH, config.VIDEO_HEIGHT), Image.Resampling.LANCZOS)
                
                # Apply strong blur
                img = img.filter(ImageFilter.GaussianBlur(radius=15))
                
                # Save blurred version
                blurred_path = image_path.parent / f"blurred_{image_path.name}"
                img.save(blurred_path)
                
                return blurred_path
                
        except Exception as e:
            logger.error(f"Failed to apply blur: {str(e)}")
            return image_path

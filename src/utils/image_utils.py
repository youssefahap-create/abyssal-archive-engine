import requests
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

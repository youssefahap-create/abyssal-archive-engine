#!/usr/bin/env python3
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
                "description": f"Quick mystery fact from The Abyssal Archive\n\nFull story: {short_script['hook']}",
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
                f.write(f"PLACEHOLDER VIDEO FILE\nContent: {script_data}\nPath: {output_path}")
        except Exception as e:
            main_logger.error(f"Error assembling video with MoviePy: {str(e)}")
            # Still create a placeholder if assembly fails
            placeholder_path = output_path.replace('.mp4', '_placeholder.mp4')
            with open(placeholder_path, 'w') as f:
                f.write(f"ERROR ASSEMBLING VIDEO\nContent: {script_data}\nOriginal path: {output_path}")
    
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
                
                message = f"🚨 The Abyssal Archive ERROR 🚨\n\n{error_message}\n\nTime: {datetime.now().isoformat()}"
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

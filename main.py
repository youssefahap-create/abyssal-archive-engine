#!/usr/bin/env python3
"""
YouTube Automated Channel - Main Script
Generates and uploads daily quiz content automatically
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from core.logger import logger
from core.tts_service import TTSService
from core.image_service import ImageService
from core.trend_service import TrendService
from core.video_generator import VideoGenerator
from core.youtube_uploader import YouTubeUploader
from core.seo_optimizer import SEOOptimizer

class YouTubeAutomation:
    def __init__(self):
        """Initialize all services"""
        logger.info("Initializing YouTube Automation System")
        
        # Setup directories
        config.setup_directories()
        
        # Initialize services
        self.tts_service = TTSService()
        self.image_service = ImageService()
        self.trend_service = TrendService()
        self.video_generator = VideoGenerator()
        self.youtube_uploader = YouTubeUploader()
        self.seo_optimizer = SEOOptimizer()
        
        # Today's content storage
        self.today_shorts = []
        self.today_compilation = None
        
        logger.info("All services initialized successfully")
    
    def generate_daily_content(self):
        """Generate all daily content"""
        logger.info(f"Generating content for {config.today_str}")
        
        # Get trending topics
        logger.info("Fetching trending topics...")
        trends = self.trend_service.get_trending_topics(count=config.DAILY_SHORTS_COUNT * 2)
        
        if not trends:
            logger.warning("No trends found, using fallback questions")
            trends = self._get_fallback_questions()
        
        # Generate shorts
        logger.info(f"Generating {config.DAILY_SHORTS_COUNT} shorts...")
        
        for i in range(config.DAILY_SHORTS_COUNT):
            if i >= len(trends):
                break
            
            logger.info(f"Generating short #{i+1}...")
            
            # Convert trend to question
            question_data = self.trend_service.convert_to_question(trends[i])
            
            # Generate short
            short_data = self._generate_single_short(question_data, index=i)
            if short_data:
                self.today_shorts.append(short_data)
                logger.info(f"Short #{i+1} generated successfully")
        
        # Generate compilation
        logger.info("Generating compilation video...")
        self._generate_compilation()
        
        logger.info(f"Daily content generation complete: {len(self.today_shorts)} shorts")
    
    def _generate_single_short(self, question_data: Dict, index: int) -> Optional[Dict]:
        """Generate a single short video"""
        
        try:
            # Generate speech
            full_text = f"{question_data['question']}. {random.choice(config.MOTIVATIONAL_PHRASES)}"
            audio_path = self.tts_service.generate_speech(full_text)
            
            if not audio_path:
                logger.error(f"Failed to generate audio for short #{index+1}")
                return None
            
            # Get image
            image_path = self.image_service.get_question_image(
                question_data["question_type"],
                question_data.get("source_topic", "")
            )
            
            if not image_path:
                logger.error(f"Failed to get image for short #{index+1}")
                return None
            
            # Generate video
            video_path = self.video_generator.create_short_video(
                question_data,
                image_path,
                audio_path
            )
            
            if not video_path:
                logger.error(f"Failed to create video for short #{index+1}")
                return None
            
            # Generate SEO metadata
            metadata = self.seo_optimizer.generate_metadata(question_data, index)
            metadata["video_path"] = video_path
            metadata["question_data"] = question_data
            
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to generate short #{index+1}: {str(e)}")
            return None
    
    def _generate_compilation(self):
        """Generate compilation video"""
        
        if len(self.today_shorts) < 2:
            logger.warning("Not enough shorts for compilation")
            return
        
        try:
            # Get video paths from shorts
            video_paths = []
            for short in self.today_shorts:
                if "video_path" in short and short["video_path"].exists():
                    video_paths.append(short["video_path"])
            
            if len(video_paths) < 2:
                logger.warning("Not enough valid videos for compilation")
                return
            
            # Generate compilation
            compilation_path = self.video_generator.create_compilation_video(video_paths)
            
            if compilation_path:
                # Generate metadata
                metadata = self.seo_optimizer.generate_compilation_metadata(self.today_shorts)
                metadata["video_path"] = compilation_path
                
                self.today_compilation = metadata
                logger.info(f"Compilation generated: {compilation_path}")
            else:
                logger.error("Failed to generate compilation video")
        
        except Exception as e:
            logger.error(f"Failed to generate compilation: {str(e)}")
    
    def upload_content(self):
        """Upload all generated content to YouTube"""
        
        if not self.today_shorts:
            logger.error("No content to upload")
            return
        
        logger.info("Starting content upload to YouTube...")
        
        try:
            # Upload shorts
            self.youtube_uploader.update_daily(self.today_shorts, self.today_compilation)
            
            logger.info("Content upload completed successfully")
            
            # Save metadata for tracking
            self._save_daily_report()
            
        except Exception as e:
            logger.error(f"Failed to upload content: {str(e)}")
    
    def _get_fallback_questions(self) -> List[Dict]:
        """Get fallback questions when no trends available"""
        
        fallback_topics = [
            {
                "title": "World Capitals Quiz",
                "description": "Test your geography knowledge",
                "source": "fallback"
            },
            {
                "title": "Famous Landmarks Challenge",
                "description": "Identify famous world monuments",
                "source": "fallback"
            },
            {
                "title": "Animal Kingdom Trivia",
                "description": "Test your animal knowledge",
                "source": "fallback"
            },
            {
                "title": "Historical Events Puzzle",
                "description": "Challenge your history knowledge",
                "source": "fallback"
            },
            {
                "title": "Scientific Discoveries Quiz",
                "description": "Test your science IQ",
                "source": "fallback"
            },
            {
                "title": "Art Masterpieces Identification",
                "description": "Identify famous artworks",
                "source": "fallback"
            },
            {
                "title": "Musical Instruments Challenge",
                "description": "Can you name these instruments?",
                "source": "fallback"
            },
            {
                "title": "World Cuisine Guessing Game",
                "description": "Identify dishes from around the world",
                "source": "fallback"
            }
        ]
        
        return fallback_topics[:config.DAILY_SHORTS_COUNT]
    
    def _save_daily_report(self):
        """Save daily generation report"""
        
        try:
            report_dir = config.LOGS_DIR / "reports"
            report_dir.mkdir(exist_ok=True)
            
            report_path = report_dir / f"report_{config.today_str}.json"
            
            report_data = {
                "date": datetime.now().isoformat(),
                "shorts_generated": len(self.today_shorts),
                "compilation_generated": self.today_compilation is not None,
                "shorts": [
                    {
                        "title": short.get("title", ""),
                        "video_path": str(short.get("video_path", "")),
                        "question": short.get("question_data", {}).get("question", "")
                    }
                    for short in self.today_shorts
                ],
                "compilation": {
                    "title": self.today_compilation.get("title", "") if self.today_compilation else "",
                    "video_path": str(self.today_compilation.get("video_path", "")) if self.today_compilation else ""
                }
            }
            
            import json
            with open(report_path, "w") as f:
                json.dump(report_data, f, indent=2)
            
            logger.info(f"Daily report saved: {report_path}")
        
        except Exception as e:
            logger.error(f"Failed to save report: {str(e)}")
    
    def cleanup_old_files(self):
        """Cleanup old generated files"""
        
        try:
            import shutil
            from datetime import datetime, timedelta
            
            cutoff_date = datetime.now() - timedelta(days=config.MAX_CACHE_DAYS)
            
            for dir_type in ["audio", "images", "videos", "shorts", "compilations"]:
                dir_path = config.STORAGE_DIR / dir_type
                
                if dir_path.exists():
                    for date_dir in dir_path.iterdir():
                        if date_dir.is_dir():
                            try:
                                dir_date = datetime.strptime(date_dir.name, "%Y%m%d")
                                if dir_date < cutoff_date:
                                    shutil.rmtree(date_dir)
                                    logger.info(f"Cleaned up old directory: {date_dir}")
                            except:
                                continue
        
        except Exception as e:
            logger.error(f"Cleanup failed: {str(e)}")

def main():
    """Main execution function"""
    
    logger.info("=" * 60)
    logger.info("YouTube Automation System Starting")
    logger.info(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    try:
        # Create automation instance
        automation = YouTubeAutomation()
        
        # Generate content
        automation.generate_daily_content()
        
        # Upload content
        automation.upload_content()
        
        # Cleanup old files
        automation.cleanup_old_files()
        
        logger.info("=" * 60)
        logger.info("YouTube Automation System Completed Successfully")
        logger.info("=" * 60)
        
        return 0
        
    except Exception as e:
        logger.critical(f"System failed: {str(e)}")
        return 1

if __name__ == "__main__":
    import random
    sys.exit(main())

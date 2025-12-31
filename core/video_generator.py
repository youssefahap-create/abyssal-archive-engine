import os
from pathlib import Path
from typing import Optional, Tuple, List
from datetime import datetime
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2

from moviepy.editor import (
    VideoClip, ImageClip, AudioFileClip,
    TextClip, CompositeVideoClip, concatenate_videoclips
)
from moviepy.video.fx.all import resize

from config import config
from core.logger import logger

class VideoGenerator:
    def __init__(self):
        # Check if font exists, download if not
        if not config.FONT_PATH.exists():
            self._setup_default_font()
    
    def _setup_default_font(self):
        """Setup default font"""
        try:
            # Try to use system font as fallback
            import matplotlib.font_manager
            fonts = matplotlib.font_manager.findSystemFonts()
            if fonts:
                config.FONT_PATH = Path(fonts[0])
            else:
                # Create a simple font file
                config.ASSETS_DIR.mkdir(parents=True, exist_ok=True)
                config.FONT_PATH = config.ASSETS_DIR / "fonts" / "default.ttf"
                config.FONT_PATH.touch()
        except:
            pass
    
    def create_short_video(self, question_data: Dict, 
                          image_path: Path, 
                          audio_path: Path) -> Optional[Path]:
        """Create a YouTube Short video"""
        
        try:
            # Create video directory
            video_dir = config.STORAGE_DIR / "videos" / config.today_str
            video_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = video_dir / f"short_{config.timestamp_str}.mp4"
            
            # Create video components
            background_clip = self._create_background_clip(image_path)
            question_clip = self._create_question_clip(question_data["question"])
            timer_clip = self._create_timer_clip()
            answer_clip = self._create_answer_clip(question_data["answer"])
            
            # Load audio
            audio_clip = AudioFileClip(str(audio_path))
            
            # Compose video
            final_clip = self._compose_video(
                background_clip,
                question_clip,
                timer_clip,
                answer_clip,
                audio_clip
            )
            
            # Write video
            final_clip.write_videofile(
                str(output_path),
                fps=config.FPS,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                verbose=False,
                logger=None
            )
            
            # Close clips
            final_clip.close()
            audio_clip.close()
            
            logger.info(f"Created short video: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to create short video: {str(e)}")
            return None
    
    def _create_background_clip(self, image_path: Path) -> ImageClip:
        """Create background clip from image"""
        try:
            # Load and resize image
            image = Image.open(image_path)
            image = image.resize((config.VIDEO_WIDTH, config.VIDEO_HEIGHT))
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Create clip
            clip = ImageClip(img_array, duration=config.SHORT_DURATION)
            return clip
            
        except Exception as e:
            logger.error(f"Failed to create background: {str(e)}")
            # Create color background as fallback
            return self._create_color_background()
    
    def _create_color_background(self) -> ImageClip:
        """Create solid color background"""
        color = tuple(int(config.BACKGROUND_COLOR[i:i+2], 16) for i in (1, 3, 5))
        frame = np.full((config.VIDEO_HEIGHT, config.VIDEO_WIDTH, 3), color, dtype=np.uint8)
        return ImageClip(frame, duration=config.SHORT_DURATION)
    
    def _create_question_clip(self, question: str) -> TextClip:
        """Create question text clip"""
        try:
            # Wrap text for better display
            wrapped_text = self._wrap_text(question, max_chars=30)
            
            # Create text clip
            txt_clip = TextClip(
                wrapped_text,
                fontsize=config.FONT_SIZE_QUESTION,
                color=config.TEXT_COLOR,
                font=str(config.FONT_PATH) if config.FONT_PATH.exists() else None,
                stroke_color=config.SECONDARY_COLOR,
                stroke_width=2,
                method='caption',
                size=(config.VIDEO_WIDTH * 0.9, config.VIDEO_HEIGHT * 0.4),
                align='center'
            )
            
            # Position in center
            txt_clip = txt_clip.set_position(('center', 'center'))
            txt_clip = txt_clip.set_duration(config.SHORT_DURATION - config.ANSWER_DURATION - 1)
            txt_clip = txt_clip.crossfadein(0.5)
            txt_clip = txt_clip.crossfadeout(0.5)
            
            return txt_clip
            
        except Exception as e:
            logger.error(f"Failed to create question clip: {str(e)}")
            # Create simple text as fallback
            return TextClip("Quiz Question", fontsize=60, color='white', duration=10)
    
    def _create_timer_clip(self) -> TextClip:
        """Create countdown timer clip"""
        
        # Create animation function
        def make_frame(t):
            # Calculate remaining time
            remaining = int(config.SHORT_DURATION - config.ANSWER_DURATION - t)
            if remaining < 0:
                remaining = 0
            
            # Create text image
            img = Image.new('RGBA', (300, 150), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype(str(config.FONT_PATH), config.FONT_SIZE_TIMER)
            except:
                font = ImageFont.load_default()
            
            # Draw timer
            timer_text = f"{remaining:02d}"
            bbox = draw.textbbox((0, 0), timer_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (300 - text_width) // 2
            y = (150 - text_height) // 2
            
            draw.text((x, y), timer_text, font=font, fill=config.ACCENT_COLOR)
            
            return np.array(img)
        
        # Create clip
        timer_clip = VideoClip(make_frame, duration=config.SHORT_DURATION - config.ANSWER_DURATION)
        timer_clip = timer_clip.set_position(('center', config.VIDEO_HEIGHT * 0.8))
        
        return timer_clip
    
    def _create_answer_clip(self, answer: str) -> TextClip:
        """Create answer reveal clip"""
        try:
            txt_clip = TextClip(
                f"Answer: {answer}",
                fontsize=config.FONT_SIZE_QUESTION,
                color=config.ACCENT_COLOR,
                font=str(config.FONT_PATH) if config.FONT_PATH.exists() else None,
                stroke_color=config.TEXT_COLOR,
                stroke_width=3,
                method='caption',
                size=(config.VIDEO_WIDTH * 0.9, config.VIDEO_HEIGHT * 0.4),
                align='center'
            )
            
            # Position and timing
            txt_clip = txt_clip.set_position(('center', 'center'))
            txt_clip = txt_clip.set_start(config.SHORT_DURATION - config.ANSWER_DURATION)
            txt_clip = txt_clip.set_duration(config.ANSWER_DURATION)
            txt_clip = txt_clip.crossfadein(0.3)
            
            return txt_clip
            
        except Exception as e:
            logger.error(f"Failed to create answer clip: {str(e)}")
            return TextClip("Answer", fontsize=60, color='red', duration=config.ANSWER_DURATION)
    
    def _compose_video(self, background: ImageClip, 
                      question: TextClip, 
                      timer: VideoClip,
                      answer: TextClip,
                      audio: AudioFileClip) -> CompositeVideoClip:
        """Compose all video elements"""
        
        # Create composite clip
        clips = [background, question, timer]
        
        # Add motivational text (appears after 5 seconds)
        motivational_text = self._create_motivational_clip()
        if motivational_text:
            motivational_text = motivational_text.set_start(5)
            clips.append(motivational_text)
        
        # Add answer at the end
        clips.append(answer)
        
        # Create composite
        final = CompositeVideoClip(clips, size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT))
        
        # Add audio
        final = final.set_audio(audio)
        final = final.set_duration(config.SHORT_DURATION)
        
        return final
    
    def _create_motivational_clip(self) -> Optional[TextClip]:
        """Create motivational text clip"""
        try:
            text = random.choice(config.MOTIVATIONAL_PHRASES)
            
            txt_clip = TextClip(
                text,
                fontsize=40,
                color=config.TEXT_COLOR,
                font=str(config.FONT_PATH) if config.FONT_PATH.exists() else None,
                stroke_color=config.SECONDARY_COLOR,
                stroke_width=1,
                method='caption',
                size=(config.VIDEO_WIDTH * 0.8, config.VIDEO_HEIGHT * 0.2),
                align='center'
            )
            
            txt_clip = txt_clip.set_position(('center', config.VIDEO_HEIGHT * 0.1))
            txt_clip = txt_clip.set_duration(3)
            
            return txt_clip
            
        except:
            return None
    
    def _wrap_text(self, text: str, max_chars: int = 30) -> str:
        """Wrap text to fit screen"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            if len(' '.join(current_line + [word])) <= max_chars:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
    
    def create_compilation_video(self, short_paths: List[Path]) -> Optional[Path]:
        """Create compilation video from shorts"""
        
        if len(short_paths) < config.COMPILATION_VIDEO_COUNT:
            logger.warning(f"Not enough shorts for compilation: {len(short_paths)}")
            return None
        
        try:
            # Load short videos
            clips = []
            for path in short_paths[:config.COMPILATION_VIDEO_COUNT]:
                try:
                    clip = VideoFileClip(str(path))
                    clips.append(clip)
                except Exception as e:
                    logger.error(f"Failed to load clip {path}: {str(e)}")
                    continue
            
            if not clips:
                return None
            
            # Create title sequence
            title_clip = self._create_title_sequence()
            if title_clip:
                clips.insert(0, title_clip)
            
            # Concatenate clips
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # Add background music
            final_clip = self._add_background_music(final_clip)
            
            # Save compilation
            compilation_dir = config.STORAGE_DIR / "compilations" / config.today_str
            compilation_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = compilation_dir / f"compilation_{config.timestamp_str}.mp4"
            
            final_clip.write_videofile(
                str(output_path),
                fps=config.FPS,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            # Close clips
            for clip in clips:
                clip.close()
            final_clip.close()
            
            logger.info(f"Created compilation video: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to create compilation: {str(e)}")
            return None
    
    def _create_title_sequence(self) -> Optional[VideoClip]:
        """Create title sequence for compilation"""
        try:
            # Create title text
            title_text = "Daily Quiz Compilation\n" + datetime.now().strftime("%B %d, %Y")
            
            txt_clip = TextClip(
                title_text,
                fontsize=80,
                color=config.ACCENT_COLOR,
                font=str(config.FONT_PATH) if config.FONT_PATH.exists() else None,
                stroke_color=config.TEXT_COLOR,
                stroke_width=2,
                method='caption',
                size=(config.VIDEO_WIDTH * 0.9, config.VIDEO_HEIGHT * 0.6),
                align='center'
            )
            
            # Create background
            bg_color = tuple(int(config.BACKGROUND_COLOR[i:i+2], 16) for i in (1, 3, 5))
            bg_frame = np.full((config.VIDEO_HEIGHT, config.VIDEO_WIDTH, 3), bg_color, dtype=np.uint8)
            bg_clip = ImageClip(bg_frame, duration=3)
            
            # Combine
            txt_clip = txt_clip.set_position(('center', 'center'))
            txt_clip = txt_clip.set_duration(3)
            txt_clip = txt_clip.crossfadein(0.5)
            txt_clip = txt_clip.crossfadeout(0.5)
            
            final = CompositeVideoClip([bg_clip, txt_clip])
            final = final.set_duration(3)
            
            return final
            
        except:
            return None
    
    def _add_background_music(self, video_clip: VideoClip) -> VideoClip:
        """Add background music to compilation"""
        try:
            # Try to add subtle background music
            # For now, just return original clip
            # In production, you would add royalty-free music
            return video_clip
        except:
            return video_clip

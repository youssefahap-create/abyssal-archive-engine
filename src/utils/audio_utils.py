import edge_tts
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

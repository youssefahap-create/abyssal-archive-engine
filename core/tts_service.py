import os
import tempfile
from pathlib import Path
from typing import Optional, Tuple
import requests
import json
from elevenlabs import generate as elevenlabs_generate
import openai
from groq import Groq
from gtts import gTTS
import pyttsx3
import io

from config import config
from core.logger import logger

class TTSService:
    def __init__(self):
        self.elevenlabs_keys = [
            os.getenv("ELEVEN_API_KEY_1"),
            os.getenv("ELEVEN_API_KEY_2"),
            os.getenv("ELEVEN_API_KEY_3")
        ]
        self.groq_client = None
        self.openai_client = None
        self.pyttsx_engine = None
        
        if os.getenv("GROQ_API_KEY"):
            self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        if os.getenv("OPENAI_API_KEY_1"):
            openai.api_key = os.getenv("OPENAI_API_KEY_1")
            self.openai_client = openai
    
    def generate_speech(self, text: str, voice_id: str = "Rachel") -> Optional[Path]:
        """Generate speech audio with fallback providers"""
        
        for provider in config.TTS_PROVIDERS:
            try:
                if provider == "elevenlabs":
                    audio_path = self._elevenlabs_tts(text, voice_id)
                    if audio_path:
                        logger.info(f"Successfully generated TTS with ElevenLabs: {text[:50]}...")
                        return audio_path
                
                elif provider == "groq" and self.groq_client:
                    audio_path = self._groq_tts(text)
                    if audio_path:
                        logger.info(f"Successfully generated TTS with Groq: {text[:50]}...")
                        return audio_path
                
                elif provider == "openai" and self.openai_client:
                    audio_path = self._openai_tts(text)
                    if audio_path:
                        logger.info(f"Successfully generated TTS with OpenAI: {text[:50]}...")
                        return audio_path
                
                elif provider == "gtts":
                    audio_path = self._gtts_tts(text)
                    if audio_path:
                        logger.info(f"Successfully generated TTS with gTTS: {text[:50]}...")
                        return audio_path
                
                elif provider == "pyttsx3":
                    audio_path = self._pyttsx3_tts(text)
                    if audio_path:
                        logger.info(f"Successfully generated TTS with pyttsx3: {text[:50]}...")
                        return audio_path
                        
            except Exception as e:
                logger.warning(f"TTS provider {provider} failed: {str(e)}")
                continue
        
        logger.error("All TTS providers failed")
        return None
    
    def _elevenlabs_tts(self, text: str, voice_id: str) -> Optional[Path]:
        """Generate speech using ElevenLabs"""
        for api_key in self.elevenlabs_keys:
            if not api_key:
                continue
            
            try:
                audio = elevenlabs_generate(
                    text=text,
                    voice=voice_id,
                    api_key=api_key
                )
                
                # Save audio to file
                audio_dir = config.STORAGE_DIR / "audio" / config.today_str
                audio_dir.mkdir(parents=True, exist_ok=True)
                
                audio_path = audio_dir / f"tts_{config.timestamp_str}.mp3"
                
                with open(audio_path, "wb") as f:
                    for chunk in audio:
                        f.write(chunk)
                
                return audio_path
                
            except Exception as e:
                logger.warning(f"ElevenLabs API key failed: {str(e)}")
                continue
        
        return None
    
    def _groq_tts(self, text: str) -> Optional[Path]:
        """Generate speech using Groq API"""
        try:
            response = self.groq_client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text,
                response_format="mp3"
            )
            
            audio_dir = config.STORAGE_DIR / "audio" / config.today_str
            audio_dir.mkdir(parents=True, exist_ok=True)
            
            audio_path = audio_dir / f"tts_{config.timestamp_str}.mp3"
            
            with open(audio_path, "wb") as f:
                f.write(response.content)
            
            return audio_path
            
        except Exception as e:
            logger.error(f"Groq TTS failed: {str(e)}")
            return None
    
    def _openai_tts(self, text: str) -> Optional[Path]:
        """Generate speech using OpenAI TTS"""
        try:
            response = self.openai_client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text
            )
            
            audio_dir = config.STORAGE_DIR / "audio" / config.today_str
            audio_dir.mkdir(parents=True, exist_ok=True)
            
            audio_path = audio_dir / f"tts_{config.timestamp_str}.mp3"
            
            response.stream_to_file(str(audio_path))
            
            return audio_path
            
        except Exception as e:
            logger.error(f"OpenAI TTS failed: {str(e)}")
            return None
    
    def _gtts_tts(self, text: str) -> Optional[Path]:
        """Generate speech using gTTS (free)"""
        try:
            audio_dir = config.STORAGE_DIR / "audio" / config.today_str
            audio_dir.mkdir(parents=True, exist_ok=True)
            
            audio_path = audio_dir / f"tts_{config.timestamp_str}.mp3"
            
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(str(audio_path))
            
            return audio_path
            
        except Exception as e:
            logger.error(f"gTTS failed: {str(e)}")
            return None
    
    def _pyttsx3_tts(self, text: str) -> Optional[Path]:
        """Generate speech using pyttsx3 (offline)"""
        try:
            if self.pyttsx_engine is None:
                self.pyttsx_engine = pyttsx3.init()
                self.pyttsx_engine.setProperty('rate', 150)
                self.pyttsx_engine.setProperty('volume', 0.9)
            
            audio_dir = config.STORAGE_DIR / "audio" / config.today_str
            audio_dir.mkdir(parents=True, exist_ok=True)
            
            audio_path = audio_dir / f"tts_{config.timestamp_str}.mp3"
            
            # pyttsx3 doesn't save directly to mp3, so we use temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                self.pyttsx_engine.save_to_file(text, tmp.name)
                self.pyttsx_engine.runAndWait()
                
                # Convert to mp3 using moviepy
                from moviepy.editor import AudioFileClip
                audio_clip = AudioFileClip(tmp.name)
                audio_clip.write_audiofile(str(audio_path))
                audio_clip.close()
            
            return audio_path
            
        except Exception as e:
            logger.error(f"pyttsx3 failed: {str(e)}")
            return None

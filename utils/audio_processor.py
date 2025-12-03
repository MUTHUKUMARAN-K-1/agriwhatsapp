"""
Audio Processing Utilities
Handles audio file download, transcription, and storage
"""

import os
import requests
import speech_recognition as sr
from pydub import AudioSegment
import logging
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)

class AudioProcessor:
    def __init__(self):
        """Initialize audio processor"""
        self.temp_dir = os.path.join(os.getcwd(), 'temp_audio')
        self.output_dir = os.path.join(os.getcwd(), 'audio_output')
        
        # Create directories if they don't exist
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.recognizer = sr.Recognizer()
        
        logger.info("Audio processor initialized")
    
    def transcribe_audio(self, audio_url: str, language: str = 'en-IN') -> str:
        """
        Download and transcribe audio from URL
        
        Args:
            audio_url: URL of the audio file
            language: Language code for transcription (e.g., 'ta-IN', 'te-IN', 'hi-IN')
        
        Returns:
            Transcribed text
        """
        try:
            # Download audio file
            audio_path = self._download_audio(audio_url)
            
            if not audio_path:
                return ""
            
            # Convert to WAV format if needed
            wav_path = self._convert_to_wav(audio_path)
            
            # Transcribe
            with sr.AudioFile(wav_path) as source:
                audio_data = self.recognizer.record(source)
                
                # Use Google Speech Recognition (free)
                text = self.recognizer.recognize_google(audio_data, language=language)
                
                logger.info(f"Transcription successful: {text[:50]}...")
                
                # Clean up temporary files
                self._cleanup_file(audio_path)
                self._cleanup_file(wav_path)
                
                return text
                
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return ""
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return ""
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return ""
    
    def save_audio(self, audio_data: bytes, user_id: str) -> str:
        """
        Save audio data to file and return public URL
        
        Args:
            audio_data: Audio file bytes
            user_id: User identifier for filename
        
        Returns:
            URL to access the audio file
        """
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"response_{user_id}_{timestamp}.mp3"
            filepath = os.path.join(self.output_dir, filename)
            
            # Save audio file
            with open(filepath, 'wb') as f:
                f.write(audio_data)
            
            logger.info(f"Audio saved: {filepath}")
            
            # Return URL (you'll need to serve these files)
            # For now, return the local path
            # In production, upload to cloud storage (S3, GCS, etc.) and return public URL
            base_url = os.getenv('BASE_URL', 'http://localhost:5000')
            audio_url = f"{base_url}/audio/{filename}"
            
            return audio_url
            
        except Exception as e:
            logger.error(f"Error saving audio: {e}")
            return ""
    
    def save_audio_local(self, audio_data: bytes, user_id: str) -> str:
        """
        Save audio data to file and return local file path
        
        Args:
            audio_data: Audio file bytes
            user_id: User identifier for filename
        
        Returns:
            Local file path to the audio file
        """
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"response_{user_id}_{timestamp}.mp3"
            filepath = os.path.join(self.output_dir, filename)
            
            # Save audio file
            with open(filepath, 'wb') as f:
                f.write(audio_data)
            
            logger.info(f"Audio saved locally: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving audio: {e}")
            return ""
    
    def _download_audio(self, url: str) -> str:
        """Download audio file from URL"""
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                # Generate temporary filename
                file_hash = hashlib.md5(url.encode()).hexdigest()[:8]
                filename = f"temp_{file_hash}.ogg"
                filepath = os.path.join(self.temp_dir, filename)
                
                # Save file
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                return filepath
            else:
                logger.error(f"Failed to download audio: {response.status_code}")
                return ""
                
        except Exception as e:
            logger.error(f"Error downloading audio: {e}")
            return ""
    
    def _convert_to_wav(self, audio_path: str) -> str:
        """Convert audio file to WAV format"""
        try:
            # Load audio file
            audio = AudioSegment.from_file(audio_path)
            
            # Convert to WAV
            wav_path = audio_path.replace(os.path.splitext(audio_path)[1], '.wav')
            audio.export(wav_path, format='wav')
            
            return wav_path
            
        except Exception as e:
            logger.error(f"Error converting audio: {e}")
            return audio_path
    
    def _cleanup_file(self, filepath: str):
        """Delete temporary file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            logger.warning(f"Could not delete temporary file {filepath}: {e}")

"""
Audio Processing Utilities
Handles audio file storage for voice responses
"""

import os
import requests
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
        
        logger.info("Audio processor initialized")
    
    # Voice transcription disabled - not needed for voice output only
    """
    def transcribe_audio(self, audio_url: str, language: str = 'en-IN') -> str:
        # This method is disabled because we only send voice, not receive it
        logger.warning("Voice transcription not available in production")
        return ""
    """
    
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
    
    # Audio conversion disabled - not needed for voice output
    """
    def _convert_to_wav(self, audio_path: str) -> str:
        # Disabled - pydub not available
        return audio_path
    """
    
    def _cleanup_file(self, filepath: str):
        """Delete temporary file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            logger.warning(f"Could not delete temporary file {filepath}: {e}")


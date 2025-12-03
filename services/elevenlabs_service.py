"""
ElevenLabs Text-to-Speech Service
Handles voice synthesis for multiple languages
"""

import os
import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class ElevenLabsService:
    def __init__(self):
        """Initialize ElevenLabs API"""
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY not found in environment variables")
        
        self.base_url = "https://api.elevenlabs.io/v1"
        
        # Voice IDs for different languages
        # You need to set these in your .env file based on your ElevenLabs account
        self.voice_ids = {
            'tamil': os.getenv('ELEVENLABS_VOICE_ID_TAMIL', os.getenv('ELEVENLABS_VOICE_ID')),
            'telugu': os.getenv('ELEVENLABS_VOICE_ID_TELUGU', os.getenv('ELEVENLABS_VOICE_ID')),
            'hindi': os.getenv('ELEVENLABS_VOICE_ID_HINDI', os.getenv('ELEVENLABS_VOICE_ID')),
            'english': os.getenv('ELEVENLABS_VOICE_ID_ENGLISH', os.getenv('ELEVENLABS_VOICE_ID'))
        }
        
        logger.info("ElevenLabs service initialized successfully")
    
    def text_to_speech(self, text: str, language: str = 'english') -> Optional[bytes]:
        """
        Convert text to speech using ElevenLabs API
        
        Args:
            text: Text to convert to speech
            language: Language code (tamil, telugu, hindi, english)
        
        Returns:
            Audio data as bytes, or None if failed
        """
        try:
            # Get voice ID for the language
            voice_id = self.voice_ids.get(language, self.voice_ids['english'])
            
            if not voice_id:
                logger.error(f"No voice ID configured for language: {language}")
                return None
            
            # Prepare API request
            url = f"{self.base_url}/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",  # Best for Indian languages
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75,
                    "style": 0.0,
                    "use_speaker_boost": True
                }
            }
            
            # Make API request
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                logger.info(f"Successfully generated speech for {language}")
                return response.content
            else:
                logger.error(f"ElevenLabs API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error in text_to_speech: {e}")
            return None
    
    def get_available_voices(self):
        """
        Get list of available voices from ElevenLabs account
        Useful for finding voice IDs
        """
        try:
            url = f"{self.base_url}/voices"
            headers = {"xi-api-key": self.api_key}
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                voices = response.json().get('voices', [])
                
                logger.info(f"Found {len(voices)} available voices")
                
                # Return simplified voice list
                return [{
                    'voice_id': v['voice_id'],
                    'name': v['name'],
                    'labels': v.get('labels', {}),
                    'description': v.get('description', '')
                } for v in voices]
            else:
                logger.error(f"Error fetching voices: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting available voices: {e}")
            return []

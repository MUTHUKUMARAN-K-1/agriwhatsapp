"""
Meta WhatsApp Business API Service
Official WhatsApp Cloud API integration (Free tier: 1,000 conversations/month)
"""

import requests
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class MetaWhatsAppService:
    def __init__(self):
        """Initialize Meta WhatsApp API with credentials from environment"""
        self.token = os.getenv('META_WHATSAPP_TOKEN')
        self.phone_number_id = os.getenv('META_PHONE_NUMBER_ID')
        self.verify_token = os.getenv('META_WEBHOOK_VERIFY_TOKEN')
        
        if not all([self.token, self.phone_number_id]):
            raise ValueError("META_WHATSAPP_TOKEN and META_PHONE_NUMBER_ID required in .env")
        
        # WhatsApp Cloud API endpoint
        self.api_version = "v21.0"
        self.api_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}/messages"
        
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        logger.info("Meta WhatsApp service initialized successfully")
    
    def send_text_message(self, to_number: str, message: str) -> bool:
        """
        Send a text message via WhatsApp
        
        Args:
            to_number: Recipient's phone number (with country code, no + or spaces)
            message: Text message to send
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Clean phone number (remove whatsapp: prefix, +, spaces)
            to_number = to_number.replace('whatsapp:', '').replace('+', '').replace(' ', '')
            
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to_number,
                "type": "text",
                "text": {
                    "preview_url": False,
                    "body": message
                }
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                message_id = result.get('messages', [{}])[0].get('id')
                logger.info(f"Text message sent to {to_number}, ID: {message_id}")
                return True
            else:
                logger.error(f"Error sending text: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Exception sending text message: {e}")
            return False
    
    def send_audio_message(self, to_number: str, audio_url: str) -> bool:
        """
        Send an audio message via WhatsApp
        
        Args:
            to_number: Recipient's phone number
            audio_url: Public HTTPS URL of the audio file (MP3, AAC, AMR, OGG)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            to_number = to_number.replace('whatsapp:', '').replace('+', '').replace(' ', '')
            
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to_number,
                "type": "audio",
                "audio": {
                    "link": audio_url
                }
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                message_id = result.get('messages', [{}])[0].get('id')
                logger.info(f"Audio message sent to {to_number}, ID: {message_id}")
                return True
            else:
                logger.error(f"Error sending audio: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Exception sending audio message: {e}")
            return False
    
    def send_document(self, to_number: str, document_url: str, filename: str, caption: Optional[str] = None) -> bool:
        """Send a document file via WhatsApp"""
        try:
            to_number = to_number.replace('whatsapp:', '').replace('+', '').replace(' ', '')
            
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to_number,
                "type": "document",
                "document": {
                    "link": document_url,
                    "filename": filename
                }
            }
            
            if caption:
                payload["document"]["caption"] = caption
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"Exception sending document: {e}")
            return False
    
    def download_media(self, media_id: str) -> Optional[bytes]:
        """
        Download media file from WhatsApp servers
        
        Args:
            media_id: Media ID from incoming message
        
        Returns:
            Media file bytes, or None if failed
        """
        try:
            # Step 1: Get media URL
            media_url = f"https://graph.facebook.com/{self.api_version}/{media_id}"
            
            response = requests.get(media_url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"Failed to get media URL: {response.status_code}")
                return None
            
            data = response.json()
            download_url = data.get('url')
            
            if not download_url:
                logger.error("No download URL in response")
                return None
            
            # Step 2: Download actual media file
            media_response = requests.get(
                download_url,
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=30
            )
            
            if media_response.status_code == 200:
                logger.info(f"Successfully downloaded media {media_id}")
                return media_response.content
            else:
                logger.error(f"Failed to download media: {media_response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Exception downloading media: {e}")
            return None
    
    def mark_message_read(self, message_id: str) -> bool:
        """Mark a message as read"""
        try:
            payload = {
                "messaging_product": "whatsapp",
                "status": "read",
                "message_id": message_id
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=5
            )
            
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"Exception marking message as read: {e}")
            return False
    
    def send_template_message(self, to_number: str, template_name: str, language_code: str = "en") -> bool:
        """
        Send a pre-approved message template
        
        Args:
            to_number: Recipient's phone number
            template_name: Template name from WhatsApp Business Manager
            language_code: Language code (e.g., 'en', 'hi', 'ta')
        
        Returns:
            True if successful, False otherwise
        """
        try:
            to_number = to_number.replace('whatsapp:', '').replace('+', '').replace(' ', '')
            
            payload = {
                "messaging_product": "whatsapp",
                "to": to_number,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {
                        "code": language_code
                    }
                }
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"Template message '{template_name}' sent to {to_number}")
                return True
            else:
                logger.error(f"Error sending template: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Exception sending template message: {e}")
            return False

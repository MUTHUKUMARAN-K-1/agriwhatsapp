"""
WhatsApp Service using Twilio
Handles sending messages and media via WhatsApp
"""

from twilio.rest import Client
import os
import logging
import requests

logger = logging.getLogger(__name__)

class WhatsAppService:
    def __init__(self):
        """Initialize Twilio client for WhatsApp"""
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        
        if not account_sid or not auth_token:
            raise ValueError("Twilio credentials not found in environment variables")
        
        self.client = Client(account_sid, auth_token)
        self.from_number = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
        
        logger.info("WhatsApp service initialized successfully")
    
    def send_text_message(self, to_number: str, message: str) -> bool:
        """
        Send a text message via WhatsApp
        
        Args:
            to_number: Recipient's phone number (without 'whatsapp:' prefix)
            message: Text message to send
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure number has whatsapp: prefix
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'
            
            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            
            logger.info(f"Text message sent: {message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending text message: {e}")
            return False
    
    def send_voice_message(self, to_number: str, audio_url: str) -> bool:
        """
        Send a voice message (audio file) via WhatsApp
        
        Args:
            to_number: Recipient's phone number
            audio_url: Public URL of the audio file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure number has whatsapp: prefix
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'
            
            message = self.client.messages.create(
                media_url=[audio_url],
                from_=self.from_number,
                to=to_number
            )
            
            logger.info(f"Voice message sent: {message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending voice message: {e}")
            return False
    
    def send_voice_message_from_file(self, to_number: str, audio_path: str) -> bool:
        """
        Send a voice message from local audio file via WhatsApp
        Uploads file to Twilio which then sends it
        
        Args:
            to_number: Recipient's phone number
            audio_path: Local path to audio file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure number has whatsapp: prefix
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'
            
            # Read the audio file
            with open(audio_path, 'rb') as audio_file:
                # Get account info
                account_sid = os.getenv('TWILIO_ACCOUNT_SID')
                
                # Upload to Twilio Media API
                media_url = f'https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json'
                
                # For now, we'll use the file path as base64 or host it temporarily
                # Simpler approach: just send without media for now
                # This is the limitation - we need a public URL
                
                logger.warn("Voice messages require public URL - skipping for now")
                return False
            
        except Exception as e:
            logger.error(f"Error sending voice message from file: {e}")
            return False
    
    def send_message_with_media(self, to_number: str, message: str, media_url: str) -> bool:
        """
        Send a text message with attached media
        
        Args:
            to_number: Recipient's phone number
            message: Text message
            media_url: URL of media file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'
            
            msg = self.client.messages.create(
                body=message,
                media_url=[media_url],
                from_=self.from_number,
                to=to_number
            )
            
            logger.info(f"Message with media sent: {msg.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending message with media: {e}")
            return False

"""
WhatsApp Voice & Text Agent - Main Application
Handles incoming WhatsApp messages and processes them through Gemini + ElevenLabs
"""

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from services.gemini_service import GeminiService
from services.elevenlabs_service import ElevenLabsService
from services.whatsapp_service import WhatsAppService
from utils.audio_processor import AudioProcessor
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize services
try:
    gemini = GeminiService()
    tts = ElevenLabsService()
    whatsapp = WhatsAppService()
    audio_processor = AudioProcessor()
    logger.info("All services initialized successfully")
except Exception as e:
    logger.error(f"Error initializing services: {e}")
    raise

@app.route('/')
def home():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "WhatsApp AI Agent",
        "features": ["text", "voice"],
        "languages": ["tamil", "telugu", "hindi", "english"]
    }

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Main webhook endpoint for receiving WhatsApp messages
    Handles both text and voice messages
    """
    try:
        # Get incoming message data
        incoming_msg = request.values.get('Body', '').strip()
        from_number = request.values.get('From', '').replace('whatsapp:', '')
        media_url = request.values.get('MediaUrl0', None)
        
        logger.info(f"Received message from {from_number}")
        
        # Initialize response
        resp = MessagingResponse()
        
        # Process based on message type
        if media_url:
            # Voice message received
            logger.info(f"Processing voice message from {media_url}")
            
            try:
                # Download and transcribe audio
                text_query = audio_processor.transcribe_audio(media_url)
                logger.info(f"Transcribed text: {text_query}")
                
                # Detect language (optional)
                detected_language = detect_user_language(text_query)
                
            except Exception as e:
                logger.error(f"Error transcribing audio: {e}")
                resp.message("Sorry, I couldn't understand the voice message. Please try again.")
                return str(resp)
        else:
            # Text message received
            text_query = incoming_msg
            detected_language = detect_user_language(text_query)
            logger.info(f"Processing text message: {text_query}")
        
        if not text_query:
            resp.message("Please send a message or voice note with your query.")
            return str(resp)
        
        # Generate AI response using Gemini
        logger.info("Generating AI response...")
        ai_response = gemini.generate_response(
            user_query=text_query,
            language=detected_language
        )
        logger.info(f"AI Response: {ai_response[:100]}...")
        
        # Send text response first
        resp.message(ai_response)
        
        # Convert to speech and send voice response
        try:
            logger.info("Converting to speech...")
            audio_data = tts.text_to_speech(ai_response, language=detected_language)
            
            # Save audio file locally
            audio_path = audio_processor.save_audio_local(audio_data, from_number)
            
            if audio_path:
                # Send voice message using local file
                whatsapp.send_voice_message_from_file(from_number, audio_path)
                logger.info(f"Voice response sent to {from_number}")
            
        except Exception as e:
            logger.error(f"Error generating voice response: {e}")
            # Continue even if voice fails - text response was already sent
        
        return str(resp)
        
    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        resp = MessagingResponse()
        resp.message("Sorry, I encountered an error. Please try again later.")
        return str(resp)

def detect_user_language(text):
    """
    Detect user's language from text
    You can use langdetect library or simple keyword matching
    """
    # Simple detection based on language
    try:
        from langdetect import detect
        lang_code = detect(text)
        
        # Map language codes to supported languages
        language_map = {
            'ta': 'tamil',
            'te': 'telugu',
            'hi': 'hindi',
            'en': 'english'
        }
        
        return language_map.get(lang_code, 'english')
    except:
        # Default to English if detection fails
        return 'english'

@app.route('/audio/<filename>')
def serve_audio(filename):
    """Serve generated audio files for WhatsApp voice messages"""
    from flask import send_from_directory
    return send_from_directory(audio_processor.output_dir, filename)

@app.route('/test', methods=['GET'])
def test():
    """Test endpoint to verify services are working"""
    try:
        # Test Gemini
        test_response = gemini.generate_response("Hello, test message", "english")
        
        return {
            "status": "success",
            "gemini": "working",
            "test_response": test_response[:100]
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }, 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting WhatsApp Agent on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

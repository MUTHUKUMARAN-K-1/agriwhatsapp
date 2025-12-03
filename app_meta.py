"""
Alternative app.py using Meta WhatsApp Business API
Use this instead of the Twilio version
"""

from flask import Flask, request, jsonify
from services.gemini_service import GeminiService
from services.elevenlabs_service import ElevenLabsService
from services.meta_whatsapp_service import MetaWhatsAppService
from utils.audio_processor import AudioProcessor
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize services
try:
    gemini = GeminiService()
    tts = ElevenLabsService()
    whatsapp = MetaWhatsAppService()
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
        "service": "WhatsApp AI Agent (Meta API)",
        "features": ["text", "voice"],
        "languages": ["tamil", "telugu", "hindi", "english"],
        "api": "Meta WhatsApp Business API"
    }

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """
    Meta WhatsApp webhook endpoint
    GET: Webhook verification
    POST: Incoming messages
    """
    
    if request.method == 'GET':
        # Webhook verification
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        mode = request.args.get('hub.mode')
        
        if mode == 'subscribe' and verify_token == os.getenv('META_WEBHOOK_VERIFY_TOKEN'):
            logger.info("Webhook verified successfully")
            return challenge, 200
        else:
            logger.warning("Webhook verification failed")
            return 'Invalid verification token', 403
    
    elif request.method == 'POST':
        # Handle incoming messages
        try:
            data = request.json
            logger.info(f"Received webhook: {data}")
            
            # Extract message data
            if 'entry' not in data:
                return 'OK', 200
            
            entry = data['entry'][0]
            changes = entry.get('changes', [])
            
            if not changes:
                return 'OK', 200
            
            value = changes[0].get('value', {})
            
            # Check if it contains messages
            if 'messages' not in value:
                # Might be a status update, ignore
                return 'OK', 200
            
            message = value['messages'][0]
            message_id = message.get('id')
            from_number = message.get('from')
            message_type = message.get('type')
            
            logger.info(f"Processing {message_type} message from {from_number}")
            
            # Mark message as read
            whatsapp.mark_message_read(message_id)
            
            # Process based on message type
            text_query = None
            
            if message_type == 'text':
                # Text message
                text_query = message['text']['body']
                logger.info(f"Text message: {text_query}")
                
            elif message_type == 'audio':
                # Voice message
                audio_id = message['audio']['id']
                logger.info(f"Downloading audio: {audio_id}")
                
                # Download audio
                audio_data = whatsapp.download_media(audio_id)
                
                if audio_data:
                    # Save temporarily and transcribe
                    temp_path = audio_processor.temp_dir + f"/{audio_id}.ogg"
                    with open(temp_path, 'wb') as f:
                        f.write(audio_data)
                    
                    # Transcribe
                    text_query = audio_processor.transcribe_audio(f"file://{temp_path}")
                    logger.info(f"Transcribed: {text_query}")
                else:
                    logger.error("Failed to download audio")
                    whatsapp.send_text_message(
                        from_number,
                        "Sorry, I couldn't process your voice message. Please try again."
                    )
                    return 'OK', 200
            
            else:
                # Unsupported message type
                logger.info(f"Unsupported message type: {message_type}")
                return 'OK', 200
            
            if not text_query:
                whatsapp.send_text_message(
                    from_number,
                    "Please send a text or voice message."
                )
                return 'OK', 200
            
            # Detect language
            detected_language = detect_user_language(text_query)
            logger.info(f"Detected language: {detected_language}")
            
            # Generate AI response using Gemini
            logger.info("Generating AI response...")
            ai_response = gemini.generate_response(
                user_query=text_query,
                language=detected_language
            )
            logger.info(f"AI Response: {ai_response[:100]}...")
            
            # Send text response
            whatsapp.send_text_message(from_number, ai_response)
            
            # Convert to speech and send voice response
            try:
                logger.info("Generating voice response...")
                audio_data = tts.text_to_speech(ai_response, language=detected_language)
                
                if audio_data:
                    # Save audio and get public URL
                    audio_url = audio_processor.save_audio(audio_data, from_number)
                    
                    if audio_url:
                        # Send voice message
                        whatsapp.send_audio_message(from_number, audio_url)
                        logger.info(f"Voice response sent to {from_number}")
                
            except Exception as e:
                logger.error(f"Error generating voice response: {e}")
                # Continue even if voice fails - text was already sent
            
            return 'OK', 200
            
        except Exception as e:
            logger.error(f"Error processing webhook: {e}", exc_info=True)
            return 'OK', 200

def detect_user_language(text):
    """Detect user's language from text"""
    try:
        from langdetect import detect
        lang_code = detect(text)
        
        language_map = {
            'ta': 'tamil',
            'te': 'telugu',
            'hi': 'hindi',
            'en': 'english'
        }
        
        return language_map.get(lang_code, 'english')
    except:
        return 'english'

@app.route('/audio/<filename>')
def serve_audio(filename):
    """Serve generated audio files"""
    from flask import send_from_directory
    return send_from_directory(audio_processor.output_dir, filename)

@app.route('/test', methods=['GET'])
def test():
    """Test endpoint"""
    try:
        test_response = gemini.generate_response("Hello, test", "english")
        
        return {
            "status": "success",
            "services": {
                "gemini": "working",
                "elevenlabs": "configured",
                "meta_whatsapp": "configured"
            },
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
    
    logger.info(f"Starting WhatsApp Agent (Meta API) on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

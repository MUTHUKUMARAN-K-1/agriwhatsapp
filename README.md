# WhatsApp AI Voice & Text Agent

An intelligent WhatsApp bot that handles both text and voice queries using:
- **Google Gemini** for AI responses
- **ElevenLabs** for text-to-speech in multiple languages
- **Twilio** for WhatsApp integration

## Features

✅ Text message support  
✅ Voice message support (send & receive)  
✅ Multi-language support (Tamil, Telugu, Hindi, English)  
✅ Automatic language detection  
✅ Agricultural assistant context  

## Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- ElevenLabs account (Creator plan)
- Twilio account (free trial)
- FFmpeg installed (for audio processing)

### 2. Installation

```bash
# Clone or navigate to project directory
cd "c:/Users/Lenovo/OneDrive/Desktop/Whatsapp Agent"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy example environment file
copy .env.example .env

# Edit .env and add your API keys
notepad .env
```

Required environment variables:
- `GEMINI_API_KEY`: Your Google Gemini API key
- `ELEVENLABS_API_KEY`: Your ElevenLabs API key
- `ELEVENLABS_VOICE_ID`: Voice ID from ElevenLabs
- `TWILIO_ACCOUNT_SID`: From Twilio console
- `TWILIO_AUTH_TOKEN`: From Twilio console

### 4. Get ElevenLabs Voice IDs

```python
# Run this to see available voices
python -c "from services.elevenlabs_service import ElevenLabsService; import os; from dotenv import load_dotenv; load_dotenv(); svc = ElevenLabsService(); voices = svc.get_available_voices(); print('\n'.join([f'{v[\"name\"]}: {v[\"voice_id\"]}' for v in voices]))"
```

### 5. Run Locally

```bash
# Start the Flask server
python app.py
```

The server will start at `http://localhost:5000`

### 6. Setup Twilio WhatsApp Sandbox

1. Go to [Twilio Console](https://console.twilio.com)
2. Navigate to Messaging > Try it out > Send a WhatsApp message
3. Follow instructions to join sandbox (send code to WhatsApp number)
4. Configure webhook URL in Twilio:
   - For local testing: Use ngrok to expose localhost
   - Webhook URL: `https://your-ngrok-url.ngrok.io/webhook`

### 7. Using ngrok for Local Testing

```bash
# Install ngrok
# Download from https://ngrok.com

# Expose local server
ngrok http 5000

# Copy the HTTPS URL and paste in Twilio webhook settings
```

## Project Structure

```
whatsapp-agent/
├── app.py                      # Main Flask application
├── services/
│   ├── gemini_service.py       # Gemini AI integration
│   ├── elevenlabs_service.py   # Text-to-speech
│   └── whatsapp_service.py     # WhatsApp messaging
├── utils/
│   └── audio_processor.py      # Audio handling
├── temp_audio/                 # Temporary audio storage
├── audio_output/               # Generated audio files
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

## Usage

### Text Message
1. Send a text message to your Twilio WhatsApp number
2. Bot will respond with both text and voice

### Voice Message
1. Send a voice note to the bot
2. Bot will transcribe it, process it, and respond with voice + text

## Testing Endpoints

```bash
# Health check
curl http://localhost:5000/

# Test Gemini integration
curl http://localhost:5000/test
```

## Deployment

### Option 1: Render.com (Recommended)
1. Push code to GitHub
2. Connect GitHub repo to Render
3. Add environment variables
4. Deploy
5. Update Twilio webhook with Render URL

### Option 2: Railway.app
1. Install Railway CLI
2. `railway init`
3. `railway up`
4. Add environment variables via dashboard
5. Update Twilio webhook

## Environment Variables for Production

```env
# Update these for production
DEBUG=False
BASE_URL=https://your-app.onrender.com
```

## Cost Breakdown

| Service | Free Tier | Your Status |
|---------|-----------|-------------|
| Gemini API | 60 req/min | ✅ Free |
| ElevenLabs | 10k chars (Starter) | ✅ Creator Plan |
| Twilio | $15 trial credit | 💰 ~150-300 msgs |
| Hosting | Free tier available | ✅ Render/Railway |

## Troubleshooting

### Audio Transcription Not Working
- Install FFmpeg: `choco install ffmpeg` (Windows)
- Check audio file format compatibility

### Voice Message Not Sending
- Ensure `BASE_URL` is set correctly
- Audio files must be publicly accessible
- Check Twilio logs for errors

### API Rate Limits
- Implement caching for common queries
- Add rate limiting middleware
- Monitor API usage

## Next Steps

1. ✅ Get all API keys
2. ✅ Test locally with ngrok
3. ✅ Deploy to production
4. ⬜ Add conversation history
5. ⬜ Implement caching
6. ⬜ Add analytics

## Support

For issues or questions:
1. Check Twilio debugger for webhook errors
2. Review application logs
3. Test individual services (Gemini, ElevenLabs)

## License

MIT License - Free to use and modify

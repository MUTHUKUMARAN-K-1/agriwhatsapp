"""
Test script to verify all services are configured correctly
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("="*50)
print("WhatsApp Agent - Configuration Test")
print("="*50)
print()

# Check environment variables
print("1. Checking environment variables...")
gemini_key = os.getenv('GEMINI_API_KEY')
elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_token = os.getenv('TWILIO_AUTH_TOKEN')

checks = {
    "Gemini API Key": gemini_key,
    "ElevenLabs API Key": elevenlabs_key,
    "Twilio Account SID": twilio_sid,
    "Twilio Auth Token": twilio_token
}

for name, value in checks.items():
    if value and len(value) > 10:
        print(f"✓ {name}: Found ({value[:10]}...)")
    else:
        print(f"✗ {name}: Missing or invalid")

print()

# Test imports
print("2. Testing package imports...")
try:
    import flask
    print("✓ Flask imported successfully")
except ImportError as e:
    print(f"✗ Flask import failed: {e}")

try:
    import google.generativeai as genai
    print("✓ Google Generative AI imported successfully")
except ImportError as e:
    print(f"✗ Google Generative AI import failed: {e}")

try:
    from twilio.rest import Client
    print("✓ Twilio imported successfully")
except ImportError as e:
    print(f"✗ Twilio import failed: {e}")

try:
    import requests
    print("✓ Requests imported successfully")
except ImportError as e:
    print(f"✗ Requests import failed: {e}")

print()

# Test Gemini connection
print("3. Testing Gemini API connection...")
try:
    import google.generativeai as genai
    if gemini_key:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content("Say hello in one word")
        print(f"✓ Gemini API working! Response: {response.text[:50]}")
    else:
        print("✗ Gemini API key not found")
except Exception as e:
    print(f"✗ Gemini API test failed: {e}")

print()

# Test ElevenLabs API key
print("4. Testing ElevenLabs API key...")
if elevenlabs_key:
    print(f"✓ ElevenLabs API key configured")
else:
    print("✗ ElevenLabs API key not found")

print()

# Test Twilio credentials
print("5. Testing Twilio credentials...")
if twilio_sid and twilio_token:
    try:
        from twilio.rest import Client
        client = Client(twilio_sid, twilio_token)
        # Just creating client, not making actual API call
        print("✓ Twilio credentials configured")
    except Exception as e:
        print(f"✗ Twilio setup failed: {e}")
else:
    print("✗ Twilio credentials not found")

print()
print("="*50)
print("Configuration test complete!")
print("="*50)
print()
print("If all checks passed, you can run: python app.py")
print()

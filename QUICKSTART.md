# Twilio WhatsApp - Quick Reference Card

## 🚀 Quick Start (30 Minutes)

### 1️⃣ Sign Up (5 mins) - BROWSER OPEN
- Fill out the Twilio signup form in your browser
- Verify email & phone
- Get $15 free credit

### 2️⃣ Get Credentials (2 mins)
Once logged in, copy from dashboard:
```
Account SID: ACxxxxxxxxxxxxxxxx
Auth Token: [click to reveal]
```

### 3️⃣ Join WhatsApp Sandbox (3 mins)
1. Twilio Console → Messaging → Try WhatsApp
2. On your phone, send to **+1 415 523 8886**:
   ```
   join [your-code-shown-on-screen]
   ```

### 4️⃣ Run Setup Script (5 mins)
```bash
cd "c:\Users\Lenovo\OneDrive\Desktop\Whatsapp Agent"
setup.bat
```

This will:
- Create virtual environment
- Install dependencies
- Create .env file
- Open .env for editing

### 5️⃣ Add API Keys to .env
Edit the .env file that opens:
```env
GEMINI_API_KEY=your_gemini_key
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_VOICE_ID=your_voice_id

TWILIO_ACCOUNT_SID=ACxxxxxx  # From step 2
TWILIO_AUTH_TOKEN=xxxxxxxx   # From step 2
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

### 6️⃣ Start App (1 min)
```bash
start.bat
```
OR
```bash
venv\Scripts\activate
python app.py
```

### 7️⃣ Expose with ngrok (2 mins)
**New terminal window:**
```bash
ngrok http 5000
```
Copy the HTTPS URL shown

### 8️⃣ Configure Webhook (2 mins)
1. Back in Twilio → WhatsApp Sandbox
2. "WHEN A MESSAGE COMES IN":
   ```
   https://your-ngrok-url.ngrok.io/webhook
   ```
3. Save

### 9️⃣ Test! 🎉
Send WhatsApp to **+1 415 523 8886**

---

## 🔑 Your Credentials Checklist
- [ ] Gemini API Key
- [ ] ElevenLabs API Key
- [ ] ElevenLabs Voice ID
- [ ] Twilio Account SID
- [ ] Twilio Auth Token

---

## 🐛 Quick Troubleshooting

**No response?**
- App running? Check terminal
- ngrok running? Check other terminal
- Webhook correct? Check Twilio console

**Server error?**
- Check .env has all keys
- Check API keys are valid
- Restart app: Ctrl+C then `python app.py`

**Can't install PyAudio?**
- Skip it - not critical
- Voice recognition will use online service

---

## 📞 Important URLs

- Twilio Console: https://console.twilio.com
- WhatsApp Test Number: +1 415 523 8886
- ngrok Dashboard: http://localhost:4040

---

## 💰 Credit Usage
- $15 free credit
- ~150-300 messages
- WhatsApp: $0.005 per message
- SMS: free or low cost

Monitor: Console → Billing

---

## 🎯 After Testing Works
1. Deploy to Render/Railway
2. Update webhook to production URL
3. Consider Meta API for free forever

---

**Need help? Check the full guide:**
[twilio-setup-guide.md](file:///C:/Users/Lenovo/.gemini/antigravity/brain/149992db-8119-4c2c-9e2e-36590a864e7e/twilio-setup-guide.md)

# Render Deployment - Step by Step Guide

## 🎯 What We're Doing
Deploying your WhatsApp agent to Render.com so voice messages work!

---

## ✅ Pre-Deployment Checklist

Before we deploy, let's make sure everything is ready:

### **1. Check if Git is initialized**
```bash
cd "c:\Users\Lenovo\OneDrive\Desktop\Whatsapp Agent"
git status
```

If you see "not a git repository", run:
```bash
git init
git add .
git commit -m "Initial commit - WhatsApp Agent"
```

### **2. Create .gitignore** (Already exists ✅)
Make sure `.env` is in `.gitignore` so secrets don't get committed.

### **3. Have your API keys ready**
You'll need these for Render environment variables:
- ✅ GEMINI_API_KEY
- ✅ ELEVENLABS_API_KEY  
- ✅ ELEVENLABS_VOICE_ID
- ✅ TWILIO_ACCOUNT_SID
- ✅ TWILIO_AUTH_TOKEN

---

## 📋 Step-by-Step Deployment

### **Step 1: Sign Up / Log In to Render** (Browser open)
1. Use Google or GitHub to sign up (easiest)
2. Verify your email if needed
3. Complete profile

### **Step 2: Push to GitHub**

**If you don't have the code on GitHub yet:**

```bash
# Create a new repo on GitHub.com first, then:
cd "c:\Users\Lenovo\OneDrive\Desktop\Whatsapp Agent"

# Initialize git (if not done)
git init
git add .
git commit -m "WhatsApp Agent with Gemini & ElevenLabs"

# Add your GitHub repo
git remote add origin https://github.com/YOUR_USERNAME/whatsapp-agent.git
git branch -M main
git push -u origin main
```

### **Step 3: Create Web Service on Render**

1. **In Render Dashboard**, click "New +" → "Web Service"
2. **Connect GitHub**: Click "Connect account" → Authorize Render
3. **Select your repo**: `whatsapp-agent`
4. Click "Connect"

### **Step 4: Configure Service**

**Settings to use:**

| Setting | Value |
|---------|-------|
| **Name** | `whatsapp-agent` (or your choice) |
| **Region** | Singapore (closest to India) |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python app.py` |
| **Plan** | `Free` |

### **Step 5: Add Environment Variables**

Click **"Advanced"** → **"Add Environment Variable"**

Add each of these (copy from your `.env` file):

```
GEMINI_API_KEY=your_actual_key
ELEVENLABS_API_KEY=your_actual_key
ELEVENLABS_VOICE_ID=your_actual_voice_id
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_actual_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
PORT=10000
DEBUG=False
```

**IMPORTANT:** Set `BASE_URL` to:
```
BASE_URL=https://YOUR-APP-NAME.onrender.com
```
(You'll get the exact URL after deployment)

### **Step 6: Deploy!**

1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. Watch the logs - you'll see:
   ```
   Building...
   Installing dependencies...
   Starting application...
   ✓ Live
   ```

### **Step 7: Get Your Render URL**

Once deployed, you'll see:
```
https://whatsapp-agent.onrender.com
```

**Copy this URL!**

### **Step 8: Update Environment Variable**

1. Go to **Environment** tab in Render
2. **Edit** `BASE_URL`
3. Set to: `https://YOUR-ACTUAL-URL.onrender.com`
4. Save (it will redeploy)

### **Step 9: Update Twilio Webhook**

1. Go to https://console.twilio.com
2. Messaging → Try WhatsApp → Sandbox
3. **WHEN A MESSAGE COMES IN**:
   ```
   https://YOUR-RENDER-URL.onrender.com/webhook
   ```
4. Save

### **Step 10: Test! 🎉**

Send a WhatsApp message to **+1 415 523 8886**

You should receive:
- ✅ Text response
- ✅ **VOICE RESPONSE!** 🎊

---

## 🐛 Troubleshooting

### **Build Failed**
- Check `requirements.txt` exists
- Check all dependencies are valid
- Look at build logs for specific errors

### **Application Crashed**
- Check environment variables are set
- Check logs in Render dashboard
- Make sure PORT=10000

### **Webhook Not Working**
- Make sure URL ends with `/webhook`
- Check it's HTTPS not HTTP
- Verify in Twilio debugger

### **Voice Still Not Working**
- Check BASE_URL is set to your Render URL
- Check logs when sending message
- Verify audio files are being created

---

## 💡 Tips

### **Free Tier Info**
- ✅ 750 hours/month free
- ⚠️ Sleeps after 15 mins of inactivity
- ⚡ Wakes up on first request (takes ~30 seconds)

### **Keep It Awake** (Optional)
Use a free service like UptimeRobot to ping your URL every 10 minutes:
```
https://YOUR-APP.onrender.com/
```

### **Viewing Logs**
- Click "Logs" tab in Render dashboard
- See real-time application logs
- Debug issues easily

---

## ✅ Success Checklist

- [ ] Signed up for Render
- [ ] Pushed code to GitHub
- [ ] Connected GitHub to Render
- [ ] Created Web Service
- [ ] Added all environment variables
- [ ] Deployed successfully
- [ ] Updated BASE_URL with actual Render URL
- [ ] Updated Twilio webhook
- [ ] Tested - got text response
- [ ] Tested - got VOICE response! 🎉

---

**Ready? I'll help you through each step!** 🚀

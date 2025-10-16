# WhatsApp Bot

Minimal FastAPI app that accepts webhooks from Meta's WhatsApp Cloud API and replies using a simple responder.

Run the app:

```bash
uvicorn main:app --reload
```
---------------------------------------------------------------------------------------

ARCHITECTURE :-



                           🌍 Meta Cloud Infrastructure
                         (WhatsApp Business Platform - Cloud API)
┌──────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│   STEP 1: Message from User (You or any customer)                        │
│                                                                          │
│   ┌────────────────────────────┐                                         │
│   │        USER (Recipient)    │                                         │
│   │  👤 Your Personal Number   │                                         │
│   │  e.g., +91XXXXXXXXXX       │                                         │
│   │  Sends message via WhatsApp│                                         │
│   └───────────────┬────────────┘                                         │
│                   │                                                     │
│                   ▼                                                     │
│     Meta Cloud API receives message (Webhook Trigger)                   │
│                   │                                                     │
│                   ▼                                                     │
│   ┌───────────────────────────────────────────────────────────┐         │
│   │           Your FastAPI Backend (Webhook Server)            │         │
│   │------------------------------------------------------------│         │
│   │ URL: https://yourappdomain.com/webhook                     │         │
│   │                                                            │         │
│   │ 1️⃣ Receives message payload from Meta                      │         │
│   │ 2️⃣ Extracts message text, sender info                      │         │
│   │ 3️⃣ Calls `responder.py` for reply logic                    │         │
│   │ 4️⃣ Calls `whatsapp_api.py` to send response                │         │
│   │                                                            │         │
│   │    🔐 Auth via: ACCESS_TOKEN (Meta Token)                   │         │
│   │    Config: PHONE_NUMBER_ID, BUSINESS_ACCOUNT_ID             │         │
│   └───────────────────────────────────────────────────────────┘         │
│                   │                                                     │
│                   ▼                                                     │
│   STEP 2: Your backend sends response via Meta Graph API                │
│                   │                                                     │
│                   ▼                                                     │
│   https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages           │
│   Payload example:                                                      │
│   {                                                                    │
│     "messaging_product": "whatsapp",                                   │
│     "to": "+91XXXXXXXXXX",                                             │
│     "type": "text",                                                    │
│     "text": { "body": "Hello 👋, I’m your WhatsApp assistant!" }       │
│   }                                                                    │
│                   │                                                     │
│                   ▼                                                     │
│   STEP 3: Meta sends your message from                                  │
│   the temporary WhatsApp business number                                │
│   📞 "From" → +1 555 234 5678 (your Meta sandbox number)                │
│                                                                          │
│   STEP 4: User (you) receives this message on your phone                │
│                                                                          │
│   👤 +91XXXXXXXXXX  ←  WhatsApp message  ←  +1 555 234 5678             │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

how to start the application :

>>check all the credentials are correctly setup in .env file
>>open terminal : cd your project folder and activate the virtual environment if not activated :  venv\Scripts\activate

install all dependencies : python -m pip install -r requirements.txt

Run your FastAPI app :
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

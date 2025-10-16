# app/webhook.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from dotenv import load_dotenv
import os
import json
from .whatsapp_api import send_text_message
from .responder import generate_reply

load_dotenv()

router = APIRouter()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")


# ----------------------------
# Meta Webhook Verification (GET)
# ----------------------------
@router.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verified successfully ✅")
        return PlainTextResponse(content=challenge, status_code=200)
    else:
        print("Webhook verification failed ❌")
        return PlainTextResponse(content="Verification failed", status_code=403)


# ----------------------------
# Receive WhatsApp Messages (POST)
# ----------------------------
@router.post("/webhook")
async def receive_webhook(request: Request):
    try:
        body = await request.json()
        print("Incoming webhook:", json.dumps(body, indent=2))

        # Only handle WhatsApp Business Account messages
        if body.get("object") == "whatsapp_business_account":
            for entry in body.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})

                    messages = value.get("messages", [])
                    if not messages:
                        continue

                    # Extract message details
                    msg = messages[0]
                    msg_body = msg.get("text", {}).get("body", "")
                    from_number = msg.get("from")
                    phone_number_id = value.get("metadata", {}).get("phone_number_id")

                    # Safely get sender name
                    contacts = value.get("contacts", [])
                    sender_name = ""
                    if contacts and "profile" in contacts[0]:
                        sender_name = contacts[0]["profile"].get("name", "")

                    print(f"📩 Message from {from_number} ({sender_name}): {msg_body}")

                    # Generate reply
                    reply_text = generate_reply(msg_body, sender_name)

                    # Send reply
                    send_text_message(phone_number_id, from_number, reply_text)

        return JSONResponse(content={"status": "received"}, status_code=200)

    except Exception as e:
        print(f"Error handling webhook: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

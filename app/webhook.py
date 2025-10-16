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

# ✅ For Meta verification (GET request)
@router.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verified successfully ✅")
        return PlainTextResponse(content=challenge, status_code=200)
    else:
        return PlainTextResponse(content="Verification failed", status_code=403)


# ✅ For receiving actual messages (POST request)
@router.post("/webhook")
async def receive_webhook(request: Request):
    try:
        body = await request.json()
        print("Incoming webhook:", json.dumps(body, indent=2))

        if body.get("object") == "whatsapp_business_account":
            for entry in body.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    if messages:
                        phone_number_id = value.get("metadata", {}).get("phone_number_id")
                        from_number = messages[0]["from"]
                        msg_body = messages[0]["text"]["body"]

                        print(f"📩 Message from {from_number}: {msg_body}")

                        reply_text = generate_reply(msg_body, sender_name)
                        send_text_message(phone_number_id, from_number, reply_text)
                        sender_name = value["contacts"][0]["profile"].get("name", "")
                        


        return JSONResponse(content={"status": "received"}, status_code=200)

    except Exception as e:
        print(f"Error handling webhook: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

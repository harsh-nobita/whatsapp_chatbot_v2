# app/whatsapp_api.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

def send_text_message(phone_number_id: str, to_number: str, message_text: str):
    """
    Send a WhatsApp text message using the Meta Graph API.
    """
    url = f"https://graph.facebook.com/v20.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message_text}
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"✅ Sent reply: {message_text}")
    else:
        print(f"❌ Failed to send message: {response.status_code} - {response.text}")

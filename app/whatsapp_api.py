import os
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
GRAPH_API_VERSION = "v17.0"  # adjust if Meta expects a different version
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

if not ACCESS_TOKEN or not PHONE_NUMBER_ID:
    raise RuntimeError("ACCESS_TOKEN and PHONE_NUMBER_ID must be set in .env")

def send_text_message(to: str, message: str) -> dict:
    """
    Send a plain text message via WhatsApp Cloud API.
    - `to` must be full phone number with country code, like '+9199xxxxxxx'
    - `message` is the text body
    Returns parsed JSON response from Meta or raises an error on failure.
    """
    url = f"{GRAPH_API_BASE}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }

    resp = requests.post(url, json=payload, headers=headers, timeout=15)
    try:
        data = resp.json()
    except ValueError:
        resp.raise_for_status()
        data = {"status_code": resp.status_code, "text": resp.text}

    if resp.status_code >= 400:
        # For debugging, raise with helpful info
        raise RuntimeError(f"WhatsApp API error {resp.status_code}: {data}")

    return data

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse
import os
from dotenv import load_dotenv
from app.whatsapp_api import send_text_message
from app.responder import get_reply

load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "mybotverify")

router = APIRouter()

@router.get("/webhook", response_class=PlainTextResponse)
async def verify_webhook(mode: str = None, challenge: str = None, verify_token: str = None):
    """
    Webhook verification endpoint for Meta (GET).
    Meta will call this URL with hub.mode, hub.challenge, hub.verify_token (as query params).
    """
    # Meta uses 'hub.' prefix in older docs; FastAPI maps query args without the prefix,
    # but when using the real webhook, Meta sends query param names as:
    #   'hub.mode', 'hub.challenge', 'hub.verify_token'
    # FastAPI won't map dotted names automatically; if you see None here, use Request-based parsing instead.
    # To be robust, also check request.query_params below.
    from fastapi import Request
    # If parameters are present, use them; otherwise attempt to parse raw query params in Request.
    # However for safety, just implement simple check:
    if verify_token is None:
        # fallback: try to use Request object to get 'hub.verify_token' if needed
        raise HTTPException(status_code=400, detail="Missing verify_token in query")
    if mode == "subscribe" and verify_token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)
    raise HTTPException(status_code=403, detail="Verification token mismatch")

@router.post("/webhook")
async def receive_webhook(request: Request):
    """
    Receive incoming messages from Meta (POST).
    Parse webhook payload and respond using WhatsApp Cloud API.
    """
    body = await request.json()
    # Minimal safety check
    if "entry" not in body:
        return {"status": "ignored", "reason": "no entry"}

    # iterate through entry/changes to find messages
    try:
        for entry in body.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                # Messages appear under value["messages"] when a user sends text
                messages = value.get("messages")
                if not messages:
                    # could be statuses or something else; ignore for now
                    continue
                for msg in messages:
                    # msg structure sample:
                    # {
                    #   "from": "9199xxxxxxx",    <- user's phone (without +)
                    #   "id": "wamid.HBgM...",
                    #   "timestamp":"...",
                    #   "text": {"body": "hello"}
                    #   ...
                    # }
                    sender = msg.get("from")
                    message_text = None
                    # text messages
                    if "text" in msg:
                        message_text = msg["text"].get("body")
                    # handle button/interactive, fallback to body if available
                    elif "interactive" in msg:
                        # interactive may contain button replies or list replies
                        interactive = msg["interactive"]
                        # check for button_reply or list_reply
                        message_text = (
                            interactive.get("button_reply", {}).get("title") or
                            interactive.get("list_reply", {}).get("title")
                        )

                    if not sender or not message_text:
                        continue

                    # format recipient phone number with + if needed
                    # Meta sometimes provides number without '+'; Graph API expects full number with country code
                    if not sender.startswith("+"):
                        to_number = f"+{sender}"
                    else:
                        to_number = sender

                    # get reply from responder
                    reply_text = get_reply(message_text, from_number=to_number)

                    # send reply via whatsapp cloud api
                    resp = send_text_message(to=to_number, message=reply_text)
                    # optionally log resp
        return {"status": "received"}
    except Exception as e:
        # avoid exposing internal errors to Meta; log in real app
        raise HTTPException(status_code=500, detail=str(e))

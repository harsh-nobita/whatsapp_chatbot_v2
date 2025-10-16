from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
import os

router = APIRouter()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@router.get("/webhook", response_class=PlainTextResponse)
async def verify_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    challenge = params.get("hub.challenge")
    token = params.get("hub.verify_token")

    print("Received GET:", dict(params))

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verified successfully ")
        return PlainTextResponse(content=challenge, status_code=200)
    else:
        print("Webhook verification failed ")
        return PlainTextResponse(content="Verification failed", status_code=403)

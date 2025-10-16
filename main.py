from fastapi import FastAPI
from app.webhook import router as webhook_router

app = FastAPI(title="WhatsApp Cloud API Bot")

# include webhook router
app.include_router(webhook_router, prefix="")

@app.get("/")
def root():
    return {"message": "WhatsApp Cloud API Bot - running"}

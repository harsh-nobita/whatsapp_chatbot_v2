# app/responder.py

from .knowledge_base import query_knowledge_base

# List of greeting keywords
GREETINGS = ["hi", "hello", "hey", "hii", "good morning", "good evening"]

def generate_reply(message_text: str, sender_name: str = "") -> str:
    """
    Generates a reply for incoming WhatsApp messages.
    
    1. If message is a greeting, respond with a personalized greeting.
    2. Otherwise, query the knowledge base for an answer.
    """
    message_text_clean = message_text.strip().lower()

    # 1️⃣ Handle greetings
    if message_text_clean in GREETINGS:
        return f"👋 Hi {sender_name or 'there'}! How can I help you today? You can ask any question or type 'faq'."

    # 2️⃣ Optional: handle 'faq' keyword specifically
    if message_text_clean == "faq":
        return "Sure! Ask me anything about our services or products, and I will help you."

    # 3️⃣ Query knowledge base for all other messages
    answer = query_knowledge_base(message_text)
    
    # If knowledge base fails to provide an answer, fallback response
    if not answer or answer.strip() == "":
        return "Sorry, I couldn't find an answer to your question. Can you please rephrase?"

    return answer

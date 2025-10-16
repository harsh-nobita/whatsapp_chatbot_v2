import re

def get_reply(message_text: str, from_number: str = None) -> str:
    """
    Simple responder. Replace or extend this function with:
    - rule-based replies
    - calling OpenAI / local NLU
    - database lookups
    """
    text = message_text.strip().lower()

    # greetings
    if re.search(r'\b(hi|hello|hey|hii|good morning|good evening)\b', text):
        return "Hello 👋! I'm your WhatsApp assistant. How can I help you today?"
    # ask for help keywords
    if "help" in text or "support" in text:
        return "Sure — please tell me briefly what you need help with. Example: 'Check order status' or 'Talk to agent'."
    # quick demo: echo with acknowledgement
    return f"I received your message: \"{message_text}\". (This is an automated reply.)"

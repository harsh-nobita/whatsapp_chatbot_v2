# app/responder.py
def generate_reply(message_text: str) -> str:
    """
    Simple auto-reply logic.
    You can later make this smarter using NLP or a database.
    """
    message_text = message_text.lower()

    if "hi" in message_text or "hello" in message_text:
        return "Hi there 👋! How can I help you today?"
    elif "help" in message_text:
        return "Sure! You can ask me about our services or say 'menu' to see options."
    elif "thanks" in message_text or "thank you" in message_text:
        return "You're welcome! 😊"
    elif "menu" in message_text:
        return "Our available options:\n1️⃣ Product Info\n2️⃣ Support\n3️⃣ Contact Us"
    else:
        return "I'm not sure I understand 🤔. Please type 'help' for options."

# responder.py

def generate_reply(message_text: str, sender_name: str = ""):
    """
    Basic rule-based response generator.
    You can later extend this to use OpenAI or other AI APIs.
    """
    message_text = message_text.strip().lower()

    # Greeting keywords
    greetings = ["hi", "hello", "hey", "hii", "good morning", "good evening", "good afternoon"]

    # Check for greeting
    if message_text in greetings:
        return (
            f"👋 Hi {sender_name or 'there'}!\n\n"
            "Welcome to *Harsh's Smart Agent!* 🤖\n\n"
            "I'm here to help you. Please choose one of the options below:\n"
            "1️⃣ Know about our services\n"
            "2️⃣ Get contact details\n"
            "3️⃣ Talk to support\n\n"
            "Type a number (1–3) to continue."
        )

    # Option-based replies
    if message_text == "1":
        return "📘 We provide AI-based automation, chatbots, and data solutions."
    elif message_text == "2":
        return "📞 You can reach us at +91-9999070861 or email harshno@gmail.com"
    elif message_text == "3":
        return "💬 Please wait while we connect you to our support team."

    # Default fallback
    return "🤔 Sorry, I didn’t understand that. Please type *hi* to start again."

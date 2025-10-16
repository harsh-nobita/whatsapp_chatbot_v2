import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (like API key)
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Custom greeting (optional)
def custom_greeting(user_name: str = None) -> str:
    if user_name:
        return f"Hello {user_name}! 👋 How can I help you today?"
    else:
        return "Hello! 👋 How can I assist you today?"

def generate_reply(message: str, user_name: str = None) -> str:
    """
    Generate a smart reply using OpenAI's GPT model directly.
    No local knowledge base required.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a friendly and helpful AI assistant."},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=300
        )

        reply = response.choices[0].message.content.strip()

        # Add a greeting if user just started chatting
        if "hi" in message.lower() or "hello" in message.lower():
            greeting = custom_greeting(user_name)
            reply = f"{greeting}\n\n{reply}"

        return reply

    except Exception as e:
        print(f"Error in generate_reply: {e}")
        return "Sorry, I'm having trouble connecting to OpenAI API right now."


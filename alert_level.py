import os
from groq import Groq
from dotenv import load_dotenv

def get_alert_level(message):
    """Classifies an alert message into 'low', 'medium', or 'high' using Groq API."""
    
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set. Check your .env file.")
    
    # client = Groq(
    #     api_key=os.environ.get("GROQ_API_KEY"),
    # )
    client = Groq(
        api_key=api_key,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an AI that classifies alert messages into three levels: low, medium, and high based on severity."
            },
            {
                "role": "user",
                "content": f"Classify this alert message: {message}. Strictly return only 'low', 'medium', or 'high'."
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    alert_level = chat_completion.choices[0].message.content.strip().lower()

    if alert_level not in ["low", "medium", "high"]:
        raise ValueError(f"Unexpected alert level: {alert_level}")

    return alert_level



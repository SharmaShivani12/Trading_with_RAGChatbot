import random

# Small talk responses (you can extend this)
SMALL_TALK = {
    "hi": ["👋 Hi there!", "Hello! How can I help you today?", "Hey! What’s up?"],
    "hello": ["Hello! 👋", "Hi, good to see you!", "Hey, how can I help?"],
    "how are you": ["🙂 I’m doing great, thanks! How about you?", "I’m just a bot, but I’m running smoothly 🚀"],
    "bye": ["Goodbye! 👋", "See you later!", "Bye, have a nice day!"],
    "thanks": ["You’re welcome 🙌", "No problem!", "Glad I could help!"]
}

def check_personality(query: str):
    q_lower = query.lower()
    for key, responses in SMALL_TALK.items():
        if key in q_lower:
            return random.choice(responses)
    return None

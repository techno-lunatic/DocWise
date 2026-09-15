import ollama

from app.config import LLM_MODEL


def rewrite_query(query, messages):

    history = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in messages
        if message["role"] != "system"
    )

    prompt = f"""
Rewrite the user's latest question into a standalone search query.

Use the conversation history to resolve references such as:
"it", "its", "they", "them", "this", "that", etc.

If the question is already standalone, return it unchanged.

Conversation history:
{history}

Latest question:
{query}

Return ONLY the rewritten search query, nothing else.
"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()
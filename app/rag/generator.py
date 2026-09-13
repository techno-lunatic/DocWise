import ollama

from app.config import LLM_MODEL


def generate_answer(prompt):

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        think=False,
        stream=True
    )

    return response["message"]["content"]
import time
import ollama


def llamaChat(userInput):
    start_time = time.time()

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "user",
                "content": userInput,
            },
        ],
    )

    end_time = time.time()
    timeDiff = end_time - start_time

    return timeDiff, response["message"]["content"]

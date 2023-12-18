import openai

def get_chat_response(user_input):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=user_input,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error generating response: {e}"
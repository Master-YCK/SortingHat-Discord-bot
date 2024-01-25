# import openai
# # ChatGPT API KEY
# openai.api_key = "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"

# def get_chat_response(user_input):
#     try:
#         response = openai.completions.create(
#             model = "text-davinci-002",
#             prompt = user_input,
#             temperature = 1,
#             max_tokens=150
#         )
#         return response["choices"][0]["text"].strip()
#     except Exception as e:
#         return f"Error generating response: {e}"
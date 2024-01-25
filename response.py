#Bot message response function
def handle_response(message) -> str:
    userInput = message.lower()

    if userInput == "hello":
        return "Hello !"
    
    if userInput == "hi":
        return "Hi !"
    
    if userInput == "how are you":
        return "I'm great! How about you?"
    
    return None
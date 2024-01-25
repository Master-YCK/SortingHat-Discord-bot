#Bot message response function
def handle_response(message) -> str:
    userInput = message.lower()

    if userInput == "hello":
        return "Hello !"
    
    if userInput == "hi":
        return "Hi !"
    
    if userInput == "how are you":
        return "I'm great! How about you ?"
    
    if userInput == "i'm fine":
        return "Good to hear that !"
    
    if userInput == "who are you":  
        return "I'm Sorting Hat !!"
    
    return None
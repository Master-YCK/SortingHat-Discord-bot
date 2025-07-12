import re


# Bot message response function
def handle_response(message) -> str:
    userInput = re.sub("[^A-Za-z ]+", "", message.lower()).replace(" ", "")

    if userInput == "hello":
        return "Hello !"

    if userInput == "hi":
        return "Hi !"

    if userInput == "howareyou":
        return "I'm great! How about you ?"

    if userInput == "imfine":
        return "Good to hear that !"

    if userInput == "whoareyou":
        return "I'm Sorting Hat !!"

    return None

import random

# handling all responses
def handle_response(message:str) -> str:
    p_message = message.lower()
    
    if p_message == "greet":
        return "Hello there!"
    
    if p_message == "roll":
        return str(random.randint(1, 6))

    if p_message == "help":
        return "`This is some help message`"

    return "Confused..."
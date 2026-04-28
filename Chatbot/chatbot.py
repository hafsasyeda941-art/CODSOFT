import re
def chatbot():
    print("Chatbot: Hello! Type 'bye' to exit.")
    while True:
        user_input = input("You: ").lower()
        
        if re.search(r"bye|exit",user_input,re.IGNORECASE):
            print("Chatbot: GoodBye!")
            break
        elif "hello" in user_input or "hi" in user_input:
            print("Chatbot: Hello!")
        elif "how are you" in user_input:
            print("Chatbot: I'm doing great!")
        elif "name" in user_input:
            print("Chatbot:I can answer your questions!")
        elif "time" in user_input:
            import datetime
            print("Chatbot:",datetime.datetime.now().strftime("%H:%M:%S"))
        elif "date" in user_input:
            import datetime
            print("Chatbot:",datetime.date.today())
    
    
     
        else:
            print("Chatbot:I don't understand.Try something else.")
     
chatbot()       

from AIAssistant import Assistant


def run():
        
    assistant = Assistant() 
    chatbot_running = True

    while chatbot_running: #forever loop
        displaymessage = "Chatbot Session has started"
        assistant.ds.log(displaymessage)
        #list choice 
        menue = """
    Choices:
        1. Find definition of words or sentences
        2. Get information on a certain topic
        3. Quit
            """
        print(menue)
        assistant.ds.log(f"AI assistant: {menue}")
    
        #ask for input
        ask_user_choice = input("Please input your choice in number form (1/2) ").strip().lower()
        assistant.ds.log(f"User requested choice {ask_user_choice}.")
        if ask_user_choice == "1":
            sentence = input("Please input a phrase or a world: ")
            assistant.FindDefinition(sentence)
        elif ask_user_choice == "2":
            ask_topic = input("Input topic: ")
            ask_sentence = int(input("How much sentences?: "))

            print(assistant.Crosscheck(ask_topic, ask_sentence))
        elif ask_user_choice == "3":
            print("Thank you")
            assistant.ds.log("Thank you")
            chatbot_running = False
        else:
            print("Invalid option")
            continue

if __name__ == "__main__":
    run() # This runs ONLY if you typed 'python main.py'



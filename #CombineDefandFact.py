#CombineDefandFact

import wikipedia
import json
import requests;

#function to get info from wikipedia 
def GetInfo(topic):

    ask_sentence_length = int(input("How much sentences do you want it to be? "))

    try: 
        #Goes to wikipedia and sumarizes topic in around 2 sentences
        summary = wikipedia.summary(topic, ask_sentence_length) 
    except wikipedia.exceptions.DisambiguationError as e:
        # If there are multiple meanings, tell the user the first few options
        return f"There are many meanings for that. Did you mean: {', '.join(e.options[:3])}?"
    except wikipedia.exceptions.PageError:
        # If the topic doesn't exist at all
        return "I'm sorry, I couldn't find a Wikipedia page for that."
    except Exception:
        return "I'm having trouble connecting to Wikipedia right now."

    return summary 

#Function for finding definition of words 
def FindDefinition(): 
    sentence = input("Input words or sentences: ")

    def_list = [] #word list
    words = sentence.split()

    for word in words:
        word.lower().strip(".,!,?")
        

        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}" #API URL

        response = requests.get(url) #actually gets the info 

        data  = response.json() #json gets data into string form 

        #data is nested, so we have to get first info:

       # data[0] → The first entry found.
       #['meanings'][0] → The first part of speech (like "noun" or "verb").
       #['definitions'][0] → The first definition block.
       #['definition'] → The actual sentence defining the word.

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            continue
        else:
            definition = data[0]['meanings'][0]['definitions'][0]['definition']
        
        def_list.append(f'{word}: {definition}')

    #just a quick little display to make things look neat
    for index, word_def in enumerate(def_list):
        print(f"""
{index + 1}. {word_def}
              """)


 
chatbot_running = True

while chatbot_running: #forever loop
    #list choice 
    print("""
Choices:
    1. Find definition of words or sentences
    2. Get information on a certain topic
          """)
    
    print() #empty space for neatness
    #ask for input
    ask_user_choice = input("Please input your choice in number form (1/2) ").strip().lower()
    if ask_user_choice == "1":
        FindDefinition()
    elif ask_user_choice == "2":
        print() #empty space for neatness
        ask_topic = input("Input topic: ")
        print(GetInfo(ask_topic))
    elif ask_user_choice == "quit" or "exit":
        print("Thank you")
        chatbot_running = False
    else:
        print("Invalid option")
        continue

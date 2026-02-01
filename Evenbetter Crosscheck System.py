#Even Better Cross Check System 

#All imports
from importlib.resources import files
import wikipedia
import json
import requests;
import datetime
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

filename = "UserDataTesting.txt" 
#Save Data Function
def Imprint(document, log_user_prompt=False):  #takes an optional parameter to log initiaed user prompts
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #date time
    log_entry = f"[{timestamp}]\n \n{document}\n" 
 
    try:
        with open(filename, 'a', encoding="utf-8") as file: #changed w to a to append everything so it doesn't refresh
            #encoding='utf-8' is added to translate other stuff like emojies
            file.write(log_entry)
        print("Document saved successfully!")
        if log_user_prompt:
            print("Doucment Saved Successfuly!")
    except OSError as e:
        print(f"Error saving document: {e}")

#function to get info from wikipedia 
def GetInfo(topic, numsentence):

    try: 
        #Goes to wikipedia and sumarizes topic in around 2 sentences
        summary = wikipedia.summary(topic, numsentence) 
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        # If there are multiple meanings, tell the user the first few options
        errormessage1 = f"There are many meanings for that. Did you mean: {', '.join(e.options[:3])}?"
        Imprint(f"Ai Assistant (Disambiguation Error): {errormessage1} ")
        return errormessage1
    except wikipedia.exceptions.PageError:
        # If the topic doesn't exist at all
        errormessage2 = "I'm sorry, I couldn't find a Wikipedia page for that."
        Imprint(f"Ai Assistant (Page Error): {errormessage2}")
        return errormessage2
    except Exception:
        errormessage3 =  "I'm having trouble connecting to Wikipedia right now."
        Imprint(f"Ai Assistant (Exception): {errormessage3}")
        return errormessage3
    

#Function to check info:
def Crosscheck(info):

    ask_sentence_length = int(input("How much sentences do you want it to be? "))
    Imprint(f"User requested info on topic: {ask_topic} with length {ask_sentence_length}.")

    #we need to versions of wiki_info.
    #one version (wiki_info) will be the one that is being crossed checked, but duckduckgo formatted summary is usually 4 sentences, so to accurately compare, we 4-5 sentences in wiki info
    #the wiki_info_user is the user's actual summary. If we know that wiki_info is credible, then it can be assumed that the user's info is also credible
    wiki_info_created = GetInfo(info, 5) 
    wiki_info_user = GetInfo(info, ask_sentence_length)
    
    #removes all specfical characters
    wiki_info = "".join(char for char in wiki_info_created if char.isalnum() or char.isspace())

    #THe formatted summary that will be presented 
    formatted_summary = wiki_info_user.replace(". ", ".\n") #Replaces period with ./n to suggest new line

    #Go to DuckDuckGO API to chekc answer
    try:
        ddg_url =  f"https://api.duckduckgo.com/?q={info}&format=json"
        ddg_info = requests.get(ddg_url).json() #gets info from API and fornats into txt
        ddg_text = ddg_info.get("AbstractText", "") #now it looks for 'AbstractText, a field within API
    except requests.exceptions.RequestException as e:
        info_not_verified = f"Could only verify {info} through Wikipedia: {formatted_summary}"
        Imprint(f"AI Assitant: {info_not_verified}")
        return info_not_verified

    #wHEN it doesn't work 
    if not ddg_text:
        info_not_verified = f"\nCould only verify information on {info} through Wikipedia:\n \n{formatted_summary}"
        Imprint(f"AI Assitant: {info_not_verified}")
        return info_not_verified
    
    #create a list of words in text
    tokenswiki = word_tokenize(wiki_info.lower())
    tokensddg = word_tokenize(ddg_text.lower())

    #unique words
    unique_wiki_words = [word for word in tokenswiki if word not in stop_words]
    unique_ddg_words =  [word for word in tokensddg if word not in stop_words]
   
    #intersection
    shared_words = set(unique_wiki_words).intersection(set(unique_ddg_words))

    #total words
    total_words = set(unique_wiki_words).union(set(unique_ddg_words))
 
    #amount of words 
    count_shared_words = len(shared_words)
    count_total_words = len(total_words)
    
    #Simiarlity Checker
    calculate_simialrity = ((count_shared_words / count_total_words) * 100)
    rounded_version = round(calculate_simialrity, 2)
    

    if calculate_simialrity >= 15:
        verfied_info = f'Info verfied by other sources:\n \n{formatted_summary}\n \nSimilarity Score: {rounded_version}%'
        Imprint(f'Ai Assitant: {verfied_info}')
        return verfied_info
    else: 
        contridicting = f'Contridicting Information.\n \nWiki says {formatted_summary}\n \nDDG says {ddg_text}\n \nSimilarity Score: {rounded_version}%'
        Imprint(f'Ai Assitant: {contridicting}:')
        return contridicting
    

#Function for finding definition of words 
def FindDefinition(): 
    sentence = input("Input words or sentences: ")

    Imprint(f"Ai Assistant: User Requested definition(s) on {sentence}")

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
        formatted_list = [f"{i+1}. {item}" for i, item in enumerate(def_list)] #this is the formatted list
    
    #join them with newlines into one long string
    result = "\n".join(formatted_list)
    
    # save the entire formatted block at once
    Imprint(result, log_user_prompt=True)

    # neat display for the console
    print("\n" + result)

 
chatbot_running = True

while chatbot_running: #forever loop
    displaymessage = "Chatbot Session has started"
    Imprint(displaymessage)
    #list choice 
    menue = """
Choices:
    1. Find definition of words or sentences
    2. Get information on a certain topic
          """
    print(menue)
    Imprint(f"AI assistant: {menue}")
    
    print() #empty space for neatness
    #ask for input
    ask_user_choice = input("Please input your choice in number form (1/2) ").strip().lower()
    Imprint(f"User requested choice {ask_user_choice}.")
    if ask_user_choice == "1":
        FindDefinition()
    elif ask_user_choice == "2":
        print() #empty space for neatness
        ask_topic = input("Input topic: ")
        print(Crosscheck(ask_topic))
    elif ask_user_choice == "quit" or ask_user_choice == "exit":
        print("Thank you")
        Imprint("Thank you")
        chatbot_running = False
    else:
        print("Invalid option")
        continue

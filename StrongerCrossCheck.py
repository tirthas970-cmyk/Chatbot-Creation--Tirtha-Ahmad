#Added Cross check

#All imports
from importlib.resources import files
import wikipedia
import json
import requests;
import datetime


filename = "UserData.txt" #defined globally 
#Save Data Function
def Imprint(document, log_user_prompt=False):  #takes an optional parameter to log initiaed user prompts
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #date time
    log_entry = f"[{timestamp}]\n {document}\n" 
 
    try:
        with open(filename, 'a', encoding="utf-8") as file: #changed w to a to append everything so it doesn't refresh
            #encoding='utf-8' is added to translate other stuff like emojies
            print() 
            file.write(log_entry)
        print("Document saved successfully!")
        if log_user_prompt:
            print("Doucment Saved Successfuly!")
    except OSError as e:
        print(f"Error saving document: {e}")

#function to get info from wikipedia 
def GetInfo(topic):

    ask_sentence_length = int(input("How much sentences do you want it to be? "))
    Imprint(f"User requested info on topic: {topic} with length {ask_sentence_length}.")

    try: 
        #Goes to wikipedia and sumarizes topic in around 2 sentences
        summary = wikipedia.summary(topic, ask_sentence_length) 
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
    wiki_info = GetInfo(info)

    formatted_summary = wiki_info.replace(". ", ".\n") #Replaces period with ./n to suggest new line
   
     #used later for check
    period_count = wiki_info.count('.')

    #Go to DuckDuckGO API to chekc answer
    try:
        ddg_url =  f"https://api.duckduckgo.com/?q={info}&format=json"
        ddg_info = requests.get(ddg_url).json() #gets info from API and fornats into txt
        ddg_text = ddg_info.get("AbstractText", "") #now it looks for 'AbstractText, a field within API
    except requests.exceptions.RequestException as e:
        info_not_verified = f"Could only verify {info} through Wikipedia: {wiki_info}"
        Imprint(f"AI Assitant: {info_not_verified}")
        return info_not_verified

    #wHEN it doesn't work 
    if not ddg_text:
        info_not_verified = f"Could only verify {info} through Wikipedia: {formatted_summary}"
        Imprint(f"AI Assitant: {info_not_verified}")
        return info_not_verified
    
    #Common English words to get rid of
    stopwords = {"the", "is", "at", "which", "on", "and", "a", "of", "to", "in", "for", "with", "it", "or"}

    #create a list of words in text
    wiki_words = set(wiki_info.lower().replace(". ", '').split()) 
    ddg_words = set(ddg_text.lower().replace('.', '').split())

    #unique words
    meaningful_wiki_words = wiki_words - stopwords
    meaningful_ddg_words = ddg_words - stopwords

    #intersection
    shared_words = meaningful_wiki_words.intersection(meaningful_ddg_words)

    #total words
    total_words = meaningful_wiki_words.union(meaningful_ddg_words)
 
    #amount of words
    count_shared_words = len(shared_words)
    count_total_words = len(total_words)
    
    #Simiarlity Checker
    calculate_simialrity = ((count_shared_words / count_total_words) * 100)
    rounded_version = round(calculate_simialrity, 2)
    
    #calculate score
    verfied = False
    Contridicting = False 
    #Below is done to elimate random probability
    #The more sentences you have, the more chance the certain words are going to match, so there needs to be a threshold
    if period_count <= 2 :
        if count_shared_words >= 2:
            verfied = True
        elif  count_shared_words < 2:
            contridicting = True
    elif period_count <=7:
        if count_shared_words >= 5:
            verfied = True
        elif count_shared_words < 5:
            contridicting = True
    elif period_count <= 13:
        if count_shared_words >= 10:
            verfied = True
        elif count_shared_words < 10:
            contridicting = True
    elif period_count <= 20:
        if count_shared_words >= 15:
            verfied = True
        elif count_shared_words < 15:
            contridicting = True
    elif period_count > 20: 
        if count_shared_words >= 17:
            verfied = True
        elif count_shared_words < 17:
            contridicting = True

    if verfied:
        verfied_info = f'Info verfied by other sources:\n {formatted_summary}\nSimilarity Score: {rounded_version}%'
        Imprint(f'Ai Assitant" {verfied_info}')
        return verfied_info
    elif contridicting: 
        contridicting = f'Contridicting Information.\n Wiki says {formatted_summary}\nDDG says {ddg_text}\nSimilarity Score: {rounded_version}%'
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

    
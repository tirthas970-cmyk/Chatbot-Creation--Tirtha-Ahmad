#Chat Bot test

import json
import requests;

def FindDefinition(): 
    #sentence for now should have no puncutation and there should not be any uppercase letters
    #testing

    sentence = input("Input sentence: ")

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

Chatbot_run = True  #Forever loop
while Chatbot_run:
    FindDefinition()
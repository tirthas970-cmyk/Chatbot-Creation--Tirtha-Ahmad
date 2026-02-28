
from DataSaving import DataHandler 
import wikipedia
import requests;
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from CrossCheckLogisticRegressionModel import MLCrossCheck


class Assistant:
    def __init__(self):
        self.ds = DataHandler() #instance variable using DataSaving Class

    #Method to get info from Wiki
    def GetInfo(self, topic, numsentence):

        try: 
            #Goes to wikipedia and sumarizes topic in amount of sentences requested
            summary = wikipedia.summary(topic, numsentence) 
            return summary 
        except wikipedia.exceptions.DisambiguationError as e:
            # If there are multiple meanings, tell the user the first few options
            errormessage1 = f"There are many meanings for that. Did you mean: {', '.join(e.options[:3])}?"
            self.ds.log(f"Ai Assistant (Disambiguation Error): {errormessage1} ")
            return errormessage1
        except wikipedia.exceptions.PageError:
            # If the topic doesn't exist at all, it will
            errormessage2 = "I'm sorry, I couldn't find a Wikipedia page for that."
            self.ds.log(f"Ai Assistant (Page Error): {errormessage2}")
            return errormessage2
        except Exception:
            errormessage3 =  "I'm having trouble connecting to Wikipedia right now."
            self.ds.log(f"Ai Assistant (Exception): {errormessage3}")
            return errormessage3
        
    #cross check info 
    def Crosscheck(self, ask_topic, ask_sentence_length):

        cross_check_ML = MLCrossCheck()

        self.ds.log(f"User requested info on topic: {ask_topic} with length {ask_sentence_length}.")

        #we need two versions of wiki_info
        #Due to DuckDuckGO formatted summary being usually 4 sentences, we need a 'version' to be around 4-5 sentences, 
        #so it is accuratly cross checked.
        #wiki_info will be the one that is being crossed checked
        #wiki_info_user is the user's actual summary.
        #If we know that wiki_info is credible, then it can be assumed that the user's info is also credible
        wiki_info_created = self.GetInfo(ask_topic, 5) 
        wiki_info_user = self.GetInfo(ask_topic, ask_sentence_length)
    
        #removes all specfical characters
        wiki_info = "".join(char for char in wiki_info_created if char.isalnum() or char.isspace())

        #The formatted summary that will be printed 
        formatted_summary = wiki_info_user.replace(". ", ".\n") #Replaces period with ./n to suggest new line

        #Go to DuckDuckGO API to chekc answer
        try:
            ddg_url =  f"https://api.duckduckgo.com/?q={ask_topic}&format=json"
            ddg_info = requests.get(ddg_url).json() #gets info from API and fornats into txt
            ddg_text = ddg_info.get("AbstractText", "") #now it looks for 'AbstractText, a field within API
        except requests.exceptions.RequestException as e:
            info_not_verified = f"Could only verify {ask_topic} through Wikipedia: {formatted_summary}"
            self.ds.log(f"AI Assitant: {info_not_verified}")
            return info_not_verified
        
        print(f'ddg text {ddg_text}')

        #if it doesn't work 
        if not ddg_text:
            info_not_verified = f"\nCould only verify information on {ask_topic} through Wikipedia:\n \n{formatted_summary}"
            self.ds.log(f"AI Assitant: {info_not_verified}")
            return info_not_verified
    
        dataFrame = [wiki_info_created, ddg_text]
        result = cross_check_ML.LogisticRegPred(dataFrame)
        result_score = cross_check_ML.PredictionScore()
         
        if result == 1:
            self.ds.log(f'Information is verfied:\nHere is your summary on {ask_topic}:\n \n{formatted_summary} \nSimilarity Score: {result_score}%')
        else:
            self.ds.log(f'Information is not verfied:\nHere is your summary on {ask_topic}:\n \n{formatted_summary} \nSimilarity Score: {result_score}%')
        

    
    #Function for finding definition of words 
    def FindDefinition(self, sentence): 
    
        #main = input sentence

        self.ds.log(f"Ai Assistant: User Requested definition(s) on {sentence}")

        def_list = [] #word list
        words = sentence.split()
        for word in words:
            word = word.lower().strip(".,!,?")
        
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
        self.ds.log(result, log_user_prompt=True)

        print("\n" + result) #for console terminal

    
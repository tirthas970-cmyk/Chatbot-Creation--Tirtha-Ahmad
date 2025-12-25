#Chat Bot Test - Response Fact Based
import wikipedia

def GetInfo(topic):

    try: 
        #Goes to wikipedia and sumarizes topic in around 2 sentences
        summary = wikipedia.summary(topic, sentences=2) 
    except wikipedia.exceptions.DisambiguationError as e:
        # If there are multiple meanings, tell the user the first few options
        return f"There are many meanings for that. Did you mean: {', '.join(e.options[:3])}?"
    except wikipedia.exceptions.PageError:
        # If the topic doesn't exist at all
        return "I'm sorry, I couldn't find a Wikipedia page for that."
    except Exception:
        return "I'm having trouble connecting to Wikipedia right now."

    return summary 


chatBot_runnning = True  #Forever loop
while chatBot_runnning:
    ask_topic = input("Input Topic: ")

    print(GetInfo(ask_topic))
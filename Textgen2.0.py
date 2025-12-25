from nltk.corpus import wordnet as wn
import nltk

# downloads
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('wordnet')
nltk.download('omw-1.4')


Chatbot_run = True


def Text_Generator():
    from nltk.tokenize import word_tokenize
    from nltk import pos_tag
    from nltk.parse.generate import generate
    from nltk.grammar import CFG

    sentences = input("Input text: ")
    words = word_tokenize(sentences.lower())
    synonyms = list(wn.synsets(word) for word in words)  
    pos_tags = pos_tag(words)  

    # Extracting nouns, verbs, prepositions based on POS tags
    nouns = (word for syn, (word, tag) in enumerate(pos_tags) if tag.startswith('NN') and synonyms[syn])
    verbs = (word for syn, (word, tag) in enumerate(pos_tags) if tag.startswith('VB') and synonyms[syn])
    prepositions = (word for syn, (word, tag) in enumerate(pos_tags) if tag == 'IN' and synonyms[syn])

    # Making basic grammar
    noun_str = ' | '.join(f"'{n}'" for n in nouns) if list(
        nouns) else "'I'"  # Convert to list to check if empty
    verb_str = ' | '.join(f"'{v}'" for v in verbs) if list(verbs) else "'cant'"
    prep_str = ' | '.join(f"'{p}'" for p in prepositions) if list(
        prepositions) else "'run'"

    grammar_str = f"""
    S -> NP VP
    NP -> Det N | Det N PP
    VP -> V NP | VP PP
    PP -> P NP
    Det -> 'a' | 'the'
    N -> {noun_str}
    V -> {verb_str}
    P -> {prep_str}
    """

    grammar = CFG.fromstring(grammar_str)

    # Example: Generate sentences (optional, based on your goal)
    for sentence in generate(grammar, n=1):
        print(' '.join(sentence))


while Chatbot_run:
    Text_Generator()

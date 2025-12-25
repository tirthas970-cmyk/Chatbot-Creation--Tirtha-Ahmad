import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('wordnet')
Chatbot_run = True


def Text_Generator():

    from nltk.tokenize import word_tokenize
    from nltk import pos_tag
    from nltk.parse.generate import generate
    from nltk.grammar import CFG

    sentences = input("Input text: ")
    words = word_tokenize(sentences.lower())
    pos_tags = pos_tag(words)

    # Extracting nouns, verbs, prepositions based on POS tags

    nouns = [word for word, tag in pos_tags if tag.startswith('NN')]

    verbs = [word for word, tag in pos_tags if tag.startswith('VB')]

    prepositions = [word for word, tag in pos_tags if tag == 'IN']

    # Making basic grammar
    noun_str = ' | '.join(
        f"'{n}'" for n in nouns) if nouns else "'cat' | 'dog'"  # Example defaults
    verb_str = ' | '.join(
        f"'{v}'" for v in verbs) if verbs else "'runs' | 'eats'"
    prep_str = ' | '.join(
        f"'{p}'" for p in prepositions) if prepositions else "'in' | 'on'"

    grammar_str = f"""
    S -> NP VP
    NP -> Det N | Det N PP
    VP -> V NP | VP PP
    PP -> P NP
    Det -> "'a' | 'the'"
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

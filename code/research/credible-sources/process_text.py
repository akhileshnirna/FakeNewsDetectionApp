from pytextrank import *
import json
from nltk import download
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
download('stopwords')
download('punkt')

def find_phrases():
    # file paths
    ip = "./data/input.json"
    op1 = "./data/op1.json"
    op2 = "./data/op2.json"
    op3 = "./data/op3.json"

    # Perform statistical parsing/tagging on a document in JSON format
    with open(op1, 'w') as f:
        for graf in parse_doc(json_iter(ip)):
            f.write("%s\n" % pretty_print(graf._asdict()))

    # Collect and normalize the key phrases from a parsed document      
    graph, ranks = text_rank(op1)
    render_ranks(graph, ranks)

    with open(op2, 'w') as f:
        for rl in normalize_key_phrases(op1, ranks):
            f.write("%s\n" % pretty_print(rl._asdict()))

    # Summarize a document based on most significant sentences and key phrases
    phrases = ", ".join(set([p for p in limit_keyphrases(op2, phrase_limit=12)]))
    phrases = [phrase.strip() for phrase in phrases.split(',')]
    phrases.sort(key=lambda x: len(x.split()), reverse=True)

    # remove stop words from each phrase
    stop_words = set(stopwords.words('english'))
    for index, phrase in enumerate(phrases):
        word_tokens = word_tokenize(phrase) 
        phrase = " ".join([w for w in word_tokens if not w in stop_words])
        phrases[index] = phrase

    # select longest phrases while maximizing keyword limit for API
    phrases_list = [phrase.split() for phrase in phrases]
    phrases_final = []
    counter = 0
    for phrase in phrases_list:
        if (counter+len(phrase)) <= 15:
            phrases_final.append(" ".join(phrase))
            counter += len(phrase)
        else:
            continue

    return phrases_final
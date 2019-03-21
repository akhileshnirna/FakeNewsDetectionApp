from pytextrank import *

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

    # Calculate a significance weight for each sentence, using MinHash to approximate a Jaccard distance from key phrases determined by TextRank
    kernel = rank_kernel(op2)

    with open(op3, 'w') as f:
        for s in top_sentences(kernel, op1):
            f.write("%s\n" % pretty_print(s._asdict()))

    # Summarize a document based on most significant sentences and key phrases
    phrases = ", ".join(set([p for p in limit_keyphrases(op2, phrase_limit=12)]))
    sent_iter = sorted(limit_sentences(op3, word_limit=150), key=lambda x: x[1])
    s = []

    for sent_text, idx in sent_iter:
        s.append(make_sentence(sent_text))

    graf_text = " ".join(s)
    # print("**excerpts:** %s\n\n**keywords:** %s" % (graf_text, phrases,))
    phrases = [phrase.strip() for phrase in phrases.split(',')]
    return phrases
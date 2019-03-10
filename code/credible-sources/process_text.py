from pytextrank import *

# file paths
ip = "input.json"
op1 = "op1.json"
op2 = "op2.json"
op3 = "op3.json"

# Perform statistical parsing/tagging on a document in JSON format
# INPUTS: JSON doc for the text input
# OUTPUT: JSON format ParsedGraf(id, sha1, graf)
with open(op1, 'w') as f:
    for graf in parse_doc(json_iter(ip)):
        f.write("%s\n" % pretty_print(graf._asdict()))

# Collect and normalize the key phrases from a parsed document
# INPUTS: <stage1>
# OUTPUT: JSON format RankedLexeme(text, rank, ids, pos)        
graph, ranks = text_rank(op1)
render_ranks(graph, ranks)

with open(op2, 'w') as f:
    for rl in normalize_key_phrases(op1, ranks):
        f.write("%s\n" % pretty_print(rl._asdict()))

# Calculate a significance weight for each sentence, using MinHash to approximate a Jaccard distance from key phrases determined by TextRank
# INPUTS: <stage1> <stage2>
# OUTPUT: JSON format SummarySent(dist, idx, text)
kernel = rank_kernel(op2)

with open(op3, 'w') as f:
    for s in top_sentences(kernel, op1):
        f.write("%s\n" % pretty_print(s._asdict()))

# Summarize a document based on most significant sentences and key phrases
# INPUTS: <stage2> <stage3>
# OUTPUT: Markdown format
phrases = ", ".join(set([p for p in limit_keyphrases(op2, phrase_limit=12)]))
sent_iter = sorted(limit_sentences(op3, word_limit=150), key=lambda x: x[1])
s = []

for sent_text, idx in sent_iter:
    s.append(make_sentence(sent_text))

graf_text = " ".join(s)
print("**excerpts:** %s\n\n**keywords:** %s" % (graf_text, phrases,))
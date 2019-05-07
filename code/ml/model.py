from pytextrank import *
from eventregistry import *
import json
import os
import pickle
import tensorflow as tf
from uuid import uuid4
from nltk import download
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
download('stopwords')
download('punkt')

import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence

import retinasdk
from ml.vars import STANCE_DETECTION_DATA

from ml.util import *

class CredibleResourcesModel(object):
    def __init__(self):
        self._sources = source_uri
        self._er = EventRegistry(apiKey = EVENT_REGISTRY_API_KEY)
        self._cortical_client = retinasdk.FullClient(CORTICAL_API_KEY, apiServer="http://api.cortical.io/rest", retinaName="en_associative")
        self._uid = str(uuid4())

        self._clfPath = '../ml/models/glove100d_final.hdf5'

        self.model = load_model(self._clfPath)
        self.graph = tf.get_default_graph()

        self._preload_path = STANCE_DETECTION_DATA
        self._dataset = pickle.load(open(self._preload_path, "rb"))
        self._train_data = self._dataset["X_train"]
        self._train_labels = self._dataset["Y_train"]
        self._test_data = self._dataset["X_test"]

        self._tokenizer = self.fit_tokenizer()

    def find_phrases(self, claim_text):
        # file paths
        ip = "../ml/data/input_" + self._uid + ".json"
        op1 = "../ml/data/op1_" + self._uid + ".json"
        op2 = "../ml/data/op2_" + self._uid + ".json"
        op3 = "../ml/data/op3_" + self._uid + ".json"

        # write claim to file - used by pytextrank
        with open(ip, 'w+') as f:
            inp = {}
            inp["id"] = self._uid
            inp["text"] = claim_text
            json.dump(inp, f)

        # Perform statistical parsing/tagging on a document in JSON format
        with open(op1, 'w+') as f:
            for graf in parse_doc(json_iter(ip)):
                f.write("%s\n" % pretty_print(graf._asdict()))

        # Collect and normalize the key phrases from a parsed document
        graph, ranks = text_rank(op1)
        render_ranks(graph, ranks)

        with open(op2, 'w+') as f:
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

    def store_corpus(self, data):
        # TODO: store collected articles in MongoDB instead of json file
        corpus = []
        corpus_path = "../results/article_corpus.json"
        if not os.path.isfile(corpus_path):
            corpus.append(data)
            with open(corpus_path, mode='w') as f:
                f.write(json.dumps(corpus, indent=2))
        else:
            with open(corpus_path) as f:
                corpus_list = json.load(f)

            corpus_list.append(data)
            with open(corpus_path, mode='w') as f:
                f.write(json.dumps(corpus_list, indent=2))



    def collect_articles(self, phrase_list):
        it = QueryArticlesIter(
                keywords = QueryItems.AND(phrase_list),
                dataType = ["news"],
                keywordsLoc = "body",
                sourceUri = QueryItems.OR(self._sources),
                lang="eng",
                dateStart = datetime(2019, 1, 1)
        )

        res = it.execQuery(self._er,
                            sortBy = "rel", # sourceAlexaGlobalRank, socialScore, sourceImportance
                            maxItems = 10,
                            returnInfo = ReturnInfo(
                                articleInfo = ArticleInfoFlags(
                                    links = True,
                                    image = True,
                                    socialScore = True,
                                    sentiment = True
                                ),
                                sourceInfo = SourceInfoFlags(
                                    ranking = True
                                )
                            )
                        )

        # create json structure for storage
        data = {}
        data["uid"] = self._uid
        data["articles"] = []
        for art in res:
            data["articles"].append(art)

        # append collected data to file to build corpus
        # self.store_corpus(data)

        return data

    def get_tokenizer(self):
        return self._tokenizer

    def fit_tokenizer(self):
        import pickle
        utils = pickle.load(open("../ml/models/utils.data", "rb"))
        tokenizer = utils['tokenizer']
        self.max_words_article = utils['max_words_article']
        self.max_words_headline = utils['max_words_headline']
        # store tokenizer
        return tokenizer

    def preprocess(self, tokenize_text, doc_type):
        # padding
        # max_words_headline = 70
        # max_words_article = 1000
        if doc_type == 'headline':
            max_words = self.max_words_headline
        elif doc_type == 'body':
            max_words = self.max_words_article

        text_seq = self._tokenizer.texts_to_sequences([tokenize_text])
        text_seq = sequence.pad_sequences(text_seq, maxlen=max_words)

        return text_seq

    def predict(self, claim_text_seq, credible_text_seq):
        with self.graph.as_default():
            pred = self.model.predict([claim_text_seq, credible_text_seq])
        return pred

    def semantic_similarity(self, claim_text, article_text):
        # returns an object of metric class
        metrics = self._cortical_client.compare(json.dumps([{"text": claim_text}, {"text": article_text}])).__dict__
        return metrics

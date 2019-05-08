import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
import pickle
import numpy as np
from keras.models import load_model
import json

from ml.FakeWebsiteDetection import MLClassifier, RuleBasedClassifier
from ml.WebSpamDetection import WebSpamDetect
from ml.model import CredibleResourcesModel
from CommunityAPI import CommunityDetection
from FakeAccountAPI import FakeAccountDetection
# from FakeImageAPI import FakeImageDetection
app = Flask(__name__)
api = Api(app)
app.debug = True

model = CredibleResourcesModel()

parser = reqparse.RequestParser()
parser.add_argument('claim_text')
parser.add_argument('url')

credible_class_mappings = {
    0: 'Unrelated',
    1: 'Discussess',
    2: 'Agrees',
    3: "Disagrees"
}


class CredibleResources(Resource):
    def __init__(self, *args, **kwargs):
        pass

    def post(self):
        # use parser and find the user's query
        args = parser.parse_args()
        claim_text = args['claim_text']

        # extract important keywords
        keywords = model.find_phrases(claim_text)

        # collect articles from credible sources using EventRegistry
        df_articles = model.collect_articles(keywords)

        # preprocess input data
        claim_text_seq = model.preprocess(claim_text, "headline")

        # get stance of each article
        res = {}
        res["results"] = []
        for i in range(len(df_articles["articles"])):
            res["uid"] = df_articles["uid"]

            credible_text_seq = model.preprocess(df_articles["articles"][i]["body"], "body")

            res["results"].append({})

            res["results"][i]["article_title"] = df_articles["articles"][i]["title"]
            res["results"][i]["article_url"] = df_articles["articles"][i]["url"]

            res["results"][i]["source"] = df_articles["articles"][i]["source"]["title"]
            res["results"][i]["source_url"] = df_articles["articles"][i]["source"]["uri"]
            res["results"][i]["source_ranking"] = df_articles["articles"][i]["source"]["ranking"]["importanceRank"]

            res["results"][i]["sentiment"] = df_articles["articles"][i]["sentiment"]

            pred = model.predict(claim_text_seq, credible_text_seq)
            pred = "{0} ({1:.2f})".format(credible_class_mappings[np.argmax(pred)], np.max(pred))
            res["results"][i]["credibility_score"] = pred
            res["results"][i]["cortical_semantic_score"] = model.semantic_similarity(claim_text, df_articles["articles"][i]["body"])

        return res, 200

class FakeWebsite(Resource):
    def post(self):
        args = parser.parse_args()
        url = args['url']
        res = {}



        #rule based classification
        model2 = RuleBasedClassifier()
        features = model2.build_feature_set(url)
        res1 = model2.calculate(features)



        #ML based classification
        model1 = MLClassifier()
        ind = -2
        try:
            ind = url.index("http")
        except:
            ind = -1
        if not (ind == 0):
            url = "http://" + url
        res["data"] = model1.classify(url) | res1



        if(res['data'] == True):
            res['final'] = "Potential Phishing website."
        else:
            res['final'] = "Not a Phishing website"

        res['url'] = url

        #res["error"] = detector.grammarCheck(url)

        print("Returning data: ", res)
        return res, 200

class WebSpamCheck(Resource):
    def post(self):
        args = parser.parse_args()
        url = args['url']
        res = {}

        try:
            ind = url.index("http")
        except:
            ind = -1
        if not (ind == 0):
            url = "http://" + url

        detector = WebSpamDetect()

        res['url'] = url 
        res['words_count'] = detector.countWords(url)
        res['title_len'] = detector.getTitleLength(url)
        res['tld_data'] = detector.TLDcheck(url)
        if res['tld_data'] in detector.tlds:
            res['tld_infer'] = "Unsafe/Most Abused"
        else:
            res['tld_infer'] = "Safe"
        if res['words_count']:
            res['txt_to_anch'] = (detector.getAllTextAnchors(url)/res['words_count']) * 100
        else:
            res['txt_to_anch'] = (detector.getAllTextAnchors(url)/1) * 100
        print("Returning data: ", res)
        return res, 200


# setup API resource routing
api.add_resource(WebSpamCheck,'/spamcheck')
api.add_resource(CredibleResources, '/credible')
api.add_resource(CommunityDetection, '/community')
# api.add_resource(FakeImageDetection, '/fakeimage',  methods=[ 'POST'])
api.add_resource(FakeAccountDetection, '/fakeaccount')
api.add_resource(FakeWebsite,'/websitecheck')

if __name__ == '__main__':
    app.run(debug=True, port=3001, host="0.0.0.0")

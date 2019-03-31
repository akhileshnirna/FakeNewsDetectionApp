import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
import pickle
import numpy as np
from keras.models import load_model
import json
import pickle

from ml.model import CredibleResourcesModel
app = Flask(__name__)
api = Api(app)

model = CredibleResourcesModel()

parser = reqparse.RequestParser()
parser.add_argument('claim_text')

class CredibleResources(Resource):
    def __init__(self, *args, **kwargs):
        self._headline = 70
        self._body = 1000

    def post(self):
        # use parser and find the user's query
        args = parser.parse_args()
        claim_text = args['claim_text']

        # extract important keywords
        keywords = model.find_phrases(claim_text)

        # collect articles from credible sources using EventRegistry
        df_articles = model.collect_articles(keywords)

        # preprocess input data
        claim_text_seq = model.preprocess(claim_text, self._headline)

        # get stance of each article
        res = {}
        res["results"] = []
        for i in range(len(df_articles["articles"])):
            res["uid"] = df_articles["uid"]

            credible_text_seq = model.preprocess(df_articles["articles"][i]["body"], self._body)

            res["results"].append({})
            
            res["results"][i]["article_title"] = df_articles["articles"][i]["title"]
            res["results"][i]["article_url"] = df_articles["articles"][i]["url"]
            
            res["results"][i]["source"] = df_articles["articles"][i]["source"]["title"]
            res["results"][i]["source_url"] = df_articles["articles"][i]["source"]["uri"]
            res["results"][i]["source_ranking"] = df_articles["articles"][i]["source"]["ranking"]["importanceRank"]
            
            res["results"][i]["sentiment"] = df_articles["articles"][i]["sentiment"]

            res["results"][i]["credibility_score"] = model.predict(claim_text_seq, credible_text_seq).tolist()[0][0]
            res["results"][i]["cortical_semantic_score"] = model.semantic_similarity(claim_text, df_articles["articles"][i]["body"])

        return res, 200


# setup API resource routing
api.add_resource(CredibleResources, '/credible/')

if __name__ == '__main__':
    app.run(debug=True)
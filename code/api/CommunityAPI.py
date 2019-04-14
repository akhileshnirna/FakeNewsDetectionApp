from ml.community.main import CommunityDetectionModel
from flask_restful import Resource, Api, reqparse, abort

model = CommunityDetectionModel()

parser = reqparse.RequestParser()


parser.add_argument('user_name')

class CommunityDetection(Resource):
    def __init__(self):
        self.model = model
    
    def post(self):
        # use parser and find the user's query
        args = parser.parse_args()
        user_name = args['user_name']

        output = model.graph_it(user_name, num_friends_at_depths=[2, 2], n_clusters=3)
        res = output
        return res, 200
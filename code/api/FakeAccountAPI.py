from ml.fakeaccount.main import FakeAccountDetectionModel
from flask_restful import Resource, Api, reqparse, abort

model = FakeAccountDetectionModel()

parser = reqparse.RequestParser()
parser.add_argument('user_name')

class FakeAccountDetection(Resource):

  def __init__(self):
    self.model = model
  
  def post(self):
    args = parser.parse_args()
    user_name = args['user_name']

    result = model.predict(user_name, max_tweets=1)

    return result, 200

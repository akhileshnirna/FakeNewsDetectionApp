from ml.fakeimage.main import FakeImageDetectionModel
from flask_restful import Resource, Api, reqparse, abort
from PIL import Image
import base64 as b64
import io

model = FakeImageDetectionModel()

parser = reqparse.RequestParser()
parser.add_argument('b64_image')

class FakeImageDetection(Resource):
	def __init__(self):
		self.model = model

	def post(self):
			# use parser and find the user's query
			args = parser.parse_args()
			image = args['b64_image']

			output = model.detect(image)
			res = {}
			return res, 200

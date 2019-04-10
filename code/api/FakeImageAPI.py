from ml.fakeimage.main import FakeImageDetectionModel
from flask_restful import Resource, Api, reqparse, abort
from PIL import Image
import base64 as b64
import io

model = FakeImageDetectionModel()

parser = reqparse.RequestParser()
parser.add_argument('im_b64')

class FakeImageDetection(Resource):
    def __init__(self):
        self.model = model
    
    def post(self):
        # use parser and find the user's query
        args = parser.parse_args()
        im_b64 = b64.b64decode(args['im_b64'])
        image = Image.open(io.BytesIO(im_b64))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)


        output = model.detect(image)
        res = output
        return res, 200
### API VERSIONS ###
# API v1.0: psa-controller/info    -> get info about the API
#           psa-controller/predict -> given a request including an image, return what is the main subject of the image (pretrained densenet121)
### API VERSIONS ###

### IMPORTS ###
import io
import os
import json

import werkzeug
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
# https://github.com/jarus/flask-testing/issues/143 - cannot import name 'cached_property' from 'werkzeug' #143
werkzeug.cached_property = werkzeug.utils.cached_property

from flask import Flask, jsonify, request, url_for, flash
from flask_restplus import Api, Resource, fields, reqparse, abort
from functools import wraps # decorators

from PIL import Image
from torchvision import models
import torchvision.transforms as transforms
### IMPORTS ###

### GLOBAL VARIABLES ###
UPLOAD_FOLDER = '/home/pi/Desktop/rpiWebServer/user_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
### GLOBAL VARIABLES ###

### FLASK CONFIGURATION ###
flask_app = Flask(__name__)
flask_app.secret_key = '*************'
flask_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

authorizations = { # AAI
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
        }
    }

app = Api(app = flask_app, authorizations=authorizations,
		  version = "1.0", 
		  title = "Photography Style Analyzer", 
		  description = "Given a photograph, predict its main subject." +
                        " More info on: https://github.com/mzouros/MSc_AI_thesis/blob/main/README.md")
api = app.namespace('psa-controller', description='Photography Style Analysis Controller')
### FLASK CONFIGURATION ###

### IMAGENET PRETRAINED MODEL ###
imagenet_class_index = json.load(open('/home/pi/Desktop/rpiWebServer/imagenet_class_index.json'))
model = models.densenet121(pretrained=True)
model.eval()
### IMAGENET PRETRAINED MODEL ###

### UPLOAD PARSER ###
upload_parser = api.parser()
upload_parser.add_argument('file', location='files', required=True, type=FileStorage, help="Acceptable extensions: ['png', 'jpg', 'jpeg']")
### UPLOAD PARSER ###

### METHODS ###
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']
        if not token:
            return {'Message' : 'Token is missing'}, 403
        if token != '*************':
            return {'Message:' : 'Token is invalid'}, 401
        print('TOKEN: {}'.format(token))
        return f(*args, **kwargs)
    return decorated

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)


def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return imagenet_class_index[predicted_idx]
### METHODS ###

### CONTROLLERS ###
@api.route('/predict')
@api.expect(upload_parser)
class UploadImage(Resource):
    
    @api.doc(responses={200: 'OK', 401: 'Unauthorized', 403: 'Forbidden', 406: 'Not Acceptable'}, security='apikey')
    @token_required
    def post(filename):
        args = upload_parser.parse_args()
        file = args.get('file')
        file_extension = file.filename.split(".")[-1]
        if request.method == 'POST':
            if file_extension not in ALLOWED_EXTENSIONS:
                abort(406, "The file's extension is not allowed. Acceptable extensions: ['png', 'jpg', 'jpeg']")
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename) #check secure_filename
                img_bytes = file.read()
                class_id, class_name = get_prediction(image_bytes=img_bytes)
                # save the image
#                 file.save(os.path.join(flask_app.config['UPLOAD_FOLDER'], file.filename))
                return {'class_id': class_id, 'class_name': class_name}

@api.route('/info')
class APIInfo(Resource):
    
    def get(self):
        flask_app.logger.warning('logger')
        return {
            "API Info": "Photography Style Analyzer"
        }
### CONTROLLERS ###   

### RUN ### 
if __name__ == '__main__':
    app.run()
### RUN ### 

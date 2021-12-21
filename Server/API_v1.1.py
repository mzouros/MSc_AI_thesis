### API VERSIONS ###
##### API v1.0 ##### 
#   psa-controller/info    -> get info about the API
#   psa-controller/predict -> given a request including an image, return what is the main subject of the image (pretrained densenet121)
##### API v1.1 ##### 
#   psa-controller/api/versions        -> get info about the API Versions
#   psa-controller/predict/color       -> given a request including an image, return if it's Colorful or Black&White
#   psa-controller/predict/depth       -> given a request including an image, return if it's Deep or Shallow
#   psa-controller/predict/palette     -> given a request including an image, return its strongest colors
#   psa-controller/predict/composition -> given a request including an image, return its Composition styles
#   psa-controller/predict/type        -> given a request including an image, return its Types
### API VERSIONS ###

### IMPORTS ###
import io
import os
import json
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import werkzeug
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
# https://github.com/jarus/flask-testing/issues/143 - cannot import name 'cached_property' from 'werkzeug' #143
werkzeug.cached_property = werkzeug.utils.cached_property

#https://stackoverflow.com/questions/67496857/cannot-import-name-endpoint-from-view-func-from-flask-helpers-in-python
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
#import flask_restful

from flask import Flask, jsonify, request, url_for, flash
from flask_restplus import Api, Resource, fields, reqparse, abort
from functools import wraps # decorators

from PIL import Image
import torch
from torchvision import models
import torchvision.transforms as transforms
import torch.nn as nn
# try/except ImportError:
### IMPORTS ###

### GLOBAL VARIABLES ###
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
### GLOBAL VARIABLES ###

### FLASK CONFIGURATION ###
flask_app = Flask(__name__)
flask_app.secret_key = '*********'

authorizations = { # AAI
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
        }
    }

app = Api(app = flask_app, authorizations=authorizations,
		  version = "1.1", 
		  title = "Photography Style Analyzer", 
		  description = "Given a photograph, analyze its style in regard to its Color, Palette (dominant color), Depth of Field (DoF), Type and Composition/Technique." +
                        " More info on: https://github.com/mzouros/MSc_AI_thesis/")
api = app.namespace('psa-controller', description='Photography Style Analysis Controller')
### FLASK CONFIGURATION ###

### MODEL ###
def model(pretrained, requires_grad, out):
    model = models.resnet50(progress=True, pretrained=pretrained)
    # freeze hidden layers
    if requires_grad == False:
        for param in model.parameters():
            param.requires_grad = False
    # train hidden layers
    elif requires_grad == True:
        for param in model.parameters():
            param.requires_grad = True
    model.fc = nn.Linear(2048, out)
    return model

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

### COLOR ###
modelColor = model(pretrained=False, requires_grad=False, out=2).to(device)
checkpointColor = torch.load('/home/mzouros/Desktop/flask_dir/psa/Models/modelColor.pth')
modelColor.load_state_dict(checkpointColor['model_state_dict'])
modelColor.eval()
### COLOR ###
### DEAPTH OF FIELD ###
modelDoF = model(pretrained=False, requires_grad=False, out=2).to(device)
checkpointDoF = torch.load('/home/mzouros/Desktop/flask_dir/psa/Models/modelDoF.pth')
modelDoF.load_state_dict(checkpointDoF['model_state_dict'])
modelDoF.eval()
### DEAPTH OF FIELD ###
### PALETTE ###
modelPalette = model(pretrained=False, requires_grad=False, out=13).to(device)
checkpointPalette = torch.load('/home/mzouros/Desktop/flask_dir/psa/Models/modelPalette.pth')
modelPalette.load_state_dict(checkpointPalette['model_state_dict'])
modelPalette.eval()
### PALETTE ###
### COMPOSITION ###
modelComposition = model(pretrained=False, requires_grad=False, out=10).to(device)
checkpointComposition = torch.load('/home/mzouros/Desktop/flask_dir/psa/Models/modelComposition.pth')
modelComposition.load_state_dict(checkpointComposition['model_state_dict'])
modelComposition.eval()
### COMPOSITION ###
### TYPE ###
modelType = model(pretrained=False, requires_grad=False, out=17).to(device)
checkpointType = torch.load('/home/mzouros/Desktop/flask_dir/psa/Models/modelType.pth')
modelType.load_state_dict(checkpointType['model_state_dict'])
modelType.eval()
### TYPE ###
### MODEL ###

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
        if token != '********':
            return {'Message:' : 'Token is invalid'}, 401
        print('TOKEN: {}'.format(token))
        return f(*args, **kwargs)
    return decorated

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize((400, 400)),transforms.ToTensor()])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)

def get_color_prediction(image_bytes):
    train = pd.read_csv('/home/mzouros/Desktop/flask_dir/psa/Models/color.csv')
    classes = np.array(train.columns[2:])
    outputs = modelColor(transform_image(image_bytes=image_bytes))
    outputs = torch.sigmoid(outputs)
    outputs = outputs.detach().cpu()
    sorted_indices = np.argsort(outputs[0])
    best = sorted_indices[-1:]
    string_predicted = ' '
    for i in range(len(best)):
        string_predicted += f"{classes[best[i]]}  "
    return json.dumps({"Predicted": string_predicted})

def get_dof_prediction(image_bytes):
    train = pd.read_csv('/home/mzouros/Desktop/flask_dir/psa/Models/dof.csv')
    classes = np.array(train.columns[2:])
    outputs = modelDoF(transform_image(image_bytes=image_bytes))
    outputs = torch.sigmoid(outputs)
    outputs = outputs.detach().cpu()
    sorted_indices = np.argsort(outputs[0])
    best = sorted_indices[-1:]
    string_predicted = ' '
    for i in range(len(best)):
        string_predicted += f"{classes[best[i]]}  "
    return json.dumps({"Predicted": string_predicted})

def get_palette_prediction(image_bytes):
    train = pd.read_csv('/home/mzouros/Desktop/flask_dir/psa/Models/palette.csv')
    classes = np.array(train.columns[2:])
    outputs = modelPalette(transform_image(image_bytes=image_bytes))
    outputs = torch.sigmoid(outputs)
    outputs = outputs.detach().cpu()
    sorted_indices = np.argsort(outputs[0])
    best = sorted_indices[-3:]
    string_predicted = ' '
    for i in range(len(best)):
        string_predicted += f"{classes[best[i]]}  "
    return json.dumps({"Predicted": string_predicted})

def get_composition_prediction(image_bytes):
    train = pd.read_csv('/home/mzouros/Desktop/flask_dir/psa/Models/composition.csv')
    classes = np.array(train.columns[2:])
    outputs = modelComposition(transform_image(image_bytes=image_bytes))
    outputs = torch.sigmoid(outputs)
    outputs = outputs.detach().cpu()
    sorted_indices = np.argsort(outputs[0])
    best = sorted_indices[-3:]
    string_predicted = ' '
    for i in range(len(best)):
        string_predicted += f"{classes[best[i]]}  "
    return json.dumps({"Predicted": string_predicted})

def get_type_prediction(image_bytes):
    train = pd.read_csv('/home/mzouros/Desktop/flask_dir/psa/Models/type.csv')
    classes = np.array(train.columns[2:])
    outputs = modelType(transform_image(image_bytes=image_bytes))
    outputs = torch.sigmoid(outputs)
    outputs = outputs.detach().cpu()
    sorted_indices = np.argsort(outputs[0])
    best = sorted_indices[-3:]
    string_predicted = ' '
    for i in range(len(best)):
        string_predicted += f"{classes[best[i]]}  "
    print(f"Predicted: {string_predicted}")  
    return json.dumps({"Predicted": string_predicted})

### METHODS ###

### CONTROLLERS ###
@api.route('/api/versions')
class APIInfo(Resource):
    def get(self):
        # flask_app.logger.warning('logger')
        file = open("/home/mzouros/Desktop/flask_dir/psa/apiInfo.json")
        versionsInfo = json.load(file)
        return versionsInfo

@api.route('/predict/color')
@api.expect(upload_parser)
class UploadImageColor(Resource):
    
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
                class_id = get_color_prediction(image_bytes=img_bytes)
                return {'class_id': class_id}

@api.route('/predict/depth')
@api.expect(upload_parser)
class UploadImageDoF(Resource):
    
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
                class_id = get_dof_prediction(image_bytes=img_bytes)
                return {'class_id': class_id}

@api.route('/predict/palette')
@api.expect(upload_parser)
class UploadImagePalette(Resource):
    
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
                class_id = get_palette_prediction(image_bytes=img_bytes)
                return {'class_id': class_id}

@api.route('/predict/composition')
@api.expect(upload_parser)
class UploadImageComposition(Resource):
    
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
                class_id = get_composition_prediction(image_bytes=img_bytes)
                return {'class_id': class_id}

@api.route('/predict/type')
@api.expect(upload_parser)
class UploadImageType(Resource):
    
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
                class_id = get_type_prediction(image_bytes=img_bytes)
                return {'class_id': class_id}
### CONTROLLERS ###   

### RUN ### 
if __name__ == '__main__':
    app.run(debug=True)
### RUN ### 

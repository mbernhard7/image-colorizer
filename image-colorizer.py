from flask import Flask, request, render_template, jsonify, make_response
import PIL
import PIL.ImageOps
import pickle
import io
from fastai.vision.all import *
import fastai
import torch
import torchvision.transforms as T
from io import BytesIO
import base64
import urllib.request
import torch
app = Flask(__name__)
#set to run on CPU
torch.device("cpu")
#fetch model from Google Cloud Storage
body=urllib.request.urlopen("https://storage.googleapis.com/image-colorizer-model/export.pkl").read()
#load model
model=load_learner(BytesIO(body), cpu=True)

#serve main page
@app.route('/')
@app.route('/index')
def index():
	return render_template('main.html')

#colorize image
@app.route('/colorize', methods=['POST'])
def colorize():
	try:
		#get file and extension
		file = request.files['imageFile']
		extension=file.filename.split('.')[-1]
		#convert image to RGB and get bytes
		img = PIL.Image.open(file.stream).convert('RGB')
		img_io = BytesIO()
		img.save(img_io, extension.upper(), quality=100)
		img_io.seek(0)
		#create fastai image and make prediciton
		img_fastai = PILImage.create(img_io)
		prediction,_,probability= model.predict(img_fastai)
		img=PIL.ImageOps.invert(img)
		#encode image as base64 to send back
		encoded_img = base64.encodebytes(img_io.getvalue()).decode('ascii')
		#send response
		data={'image':"data:image/"+extension.lower()+";base64,"+encoded_img, 'prediction':prediction, 'probability':'{:0.6e}'.format(probability[1].item())}
		return make_response(jsonify(data), 200)
	except Exception as e:
		print(e)
		return f"An Error Occured: {e}",400
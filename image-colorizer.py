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

app = Flask(__name__)
import torch
torch.device("cpu")

model=load_learner(open("./models/export.pkl",'rb'), cpu=True)

@app.route('/')
@app.route('/index')
def index():
	return render_template('main.html')

@app.route('/colorize', methods=['POST'])
def colorize():
	try:
		file = request.files['imageFile']
		extension=file.filename.split('.')[-1]
		img = PIL.Image.open(file.stream).convert('RGB')
		img_io = BytesIO()
		img.save(img_io, extension.upper(), quality=100)
		img_io.seek(0)
		img_fastai = PILImage.create(img_io)
		prediction,_,probability= model.predict(img_fastai)
		img=PIL.ImageOps.invert(img)
		
		encoded_img = base64.encodebytes(img_io.getvalue()).decode('ascii') # encode as base64

		data={'image':"data:image/"+extension.lower()+";base64,"+encoded_img, 'prediction':prediction, 'probability':'{:0.6e}'.format(probability[1].item())}
		return make_response(jsonify(data), 200)
	except Exception as e:
		print(e)
		return f"An Error Occured: {e}",400
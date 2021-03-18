from flask import Flask, request, render_template, jsonify, make_response
import PIL
import PIL.ImageOps
import pickle
import io
from fastai.vision.all import *
import fastai
from io import BytesIO
import base64
import urllib.request

app = Flask(__name__)

# fetch and load model from Google Cloud Storage
model_url="https://storage.googleapis.com/image-colorizer-model/export.pkl"
body = urllib.request.urlopen(model_url).read()
model = load_learner(BytesIO(body), cpu=True)


@app.route('/')
@app.route('/index')
def index():
    """Returns the main page

    Returns:
        HTML Page: renders the main html page
    """
    return render_template('main.html')


@app.route('/colorize', methods=['POST'])
def colorize():
    """Receive an image, colorize it, and  return it in base64 encoding

    Returns:
        JSON Response: a prediction using the Pets nueral network and the image with its colors inverted
    """
    try:
        file = request.files['imageFile']
        extension = file.filename.split('.')[-1]

        # convert image to RGB and get bytes
        img = PIL.Image.open(file.stream).convert('RGB')
        img_io = BytesIO()
        img.save(img_io, extension.upper(), quality=100)

        # create fastai image and make prediciton
        img_fastai = PILImage.create(img_io)
        prediction, _, probability = model.predict(img_fastai)

        # invert image and get bytes
        img = PIL.ImageOps.invert(img)
        img_io = BytesIO()
        img.save(img_io, extension.upper(), quality=100)

        # encode image as base64 to send back
        encoded_img = base64.encodebytes(img_io.getvalue()).decode('ascii')
        data = {
            'image': "data:image/"+extension.lower()+";base64,"+encoded_img,
            'prediction': prediction,
            'probability': '{:0.6e}'.format(probability[1].item())}
        return make_response(jsonify(data), 200)

    except Exception as e:
        print(e)
        return f"An Error Occured: {e}", 400

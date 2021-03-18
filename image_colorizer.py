import urllib.request
import PIL
import PIL.ImageOps
import pickle
from fastai.vision.all import *
import fastai
from io import BytesIO
import base64

# fetch and load model from Google Cloud Storage
model_url = "https://storage.googleapis.com/image-colorizer-model/export.pkl"
body = urllib.request.urlopen(model_url).read()
model = load_learner(BytesIO(body), cpu=True)


def colorize_file(file, extension):
    """Invert image colors, make prediction using Pets NN

    Args:
        file (file-like object): file taken from post request
        extension (string): file ending

    Returns:
        Dictionairy: image data and prediction data
    """
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
    return data

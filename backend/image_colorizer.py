import urllib.request
import numpy as np
import cv2 as cv
from io import BytesIO
import os.path
import base64
import tempfile

# fetch and load model from Google Cloud Storage

with tempfile.NamedTemporaryFile(suffix='.caffemodel', dir='model/') as f:
    model_url = "https://storage.googleapis.com/image-colorizer-model/color" \
        "ization_release_v2.caffemodel"
    f.write(urllib.request.urlopen(model_url).read())
    numpy_file = np.load('./model/pts_in_hull.npy')
    Caffe_net = cv.dnn.readNetFromCaffe(
        "./model/colorization_deploy_v2.prototxt", f.name)
numpy_file = numpy_file.transpose().reshape(2, 313, 1, 1)
print(Caffe_net.getLayer(Caffe_net.getLayerId('class8_ab')).blobs)
Caffe_net.getLayer(Caffe_net.getLayerId('class8_ab')).blobs = [
    numpy_file.astype(np.float32)]
Caffe_net.getLayer(Caffe_net.getLayerId('conv8_313_rh')).blobs = [
    np.full([1, 313], 2.606, np.float32)]

def colorize_file(file, extension):
    """Colorizes the image using OpenCV model

    Args:
        file (file-like object): file taken from post request
        extension (string): file ending

    Returns:
        Dictionairy: image data
    """
    with tempfile.NamedTemporaryFile(suffix='.'+extension) as f:
        file.seek(0)
        f.write(file.read())
        f.seek(0)
        img = cv.imread(f.name, 1)

    input_width = 224
    input_height = 224
    rgb_img = (img[:, :, [2, 1, 0]] * 1.0 / 255).astype(np.float32)
    lab_img = cv.cvtColor(rgb_img, cv.COLOR_RGB2Lab)
    l_channel = lab_img[:, :, 0]
    l_channel_resize = cv.resize(l_channel, (input_width, input_height))
    l_channel_resize -= 50
    Caffe_net.setInput(cv.dnn.blobFromImage(l_channel_resize))
    ab_channel = Caffe_net.forward()[0, :, :, :].transpose((1, 2, 0))
    (original_height, original_width) = rgb_img.shape[:2]
    ab_channel_us = cv.resize(ab_channel, (original_width, original_height))
    lab_output = np.concatenate(
        (l_channel[:, :, np.newaxis], ab_channel_us), axis=2)
    bgr_output = np.clip(cv.cvtColor(lab_output, cv.COLOR_Lab2BGR), 0, 1)
    is_success, buffer = cv.imencode(
        '.'+extension, (bgr_output*255).astype(np.uint8))
    io_buf = BytesIO(buffer)
    encoded_img = base64.encodebytes(io_buf.getvalue()).decode('ascii')
    data = {
        'image': "data:image/"+extension.lower()+";base64,"+encoded_img
    }
    return data

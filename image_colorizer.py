import urllib.request
import numpy as np
import cv2 as cv
from io import BytesIO
import os.path
import base64
import tempfile
import time
from operator import itemgetter
from pympler import tracker, asizeof
# fetch and load model from Google Cloud Storage
mem = tracker.SummaryTracker()
print("start model import")
t0 = time.time()
with tempfile.NamedTemporaryFile(suffix='.caffemodel', dir='model/') as f:
    model_url = "https://storage.googleapis.com/image-colorizer-model/color" \
        "ization_release_v2.caffemodel"
    f.write(urllib.request.urlopen(model_url).read())
    numpy_file = np.load('./model/pts_in_hull.npy')
    Caffe_net = cv.dnn.readNetFromCaffe(
        "./model/colorization_deploy_v2.prototxt", f.name)
numpy_file = numpy_file.transpose().reshape(2, 313, 1, 1)
Caffe_net.getLayer(Caffe_net.getLayerId('class8_ab')).blobs = [
    numpy_file.astype(np.float32)]
Caffe_net.getLayer(Caffe_net.getLayerId('conv8_313_rh')).blobs = [
    np.full([1, 313], 2.606, np.float32)]
t1 = time.time()
total = t1-t0
print("End model import: "+str(total))
print(asizeof.asizeof(Caffe_net))
for x in sorted(mem.create_summary(), reverse=True, key=itemgetter(2))[:10]:
    print(x)


def colorize_file(file, extension):
    """Colorizes the image using OpenCV model

    Args:
        file (file-like object): file taken from post request
        extension (string): file ending

    Returns:
        Dictionairy: image data
    """
    print("start colorize")
    print(type(file))
    t0 = time.time()
    with tempfile.NamedTemporaryFile(suffix='.'+extension) as f:
        file.save(f)
        file.close()
        img = cv.imread(f.name)
    for x in sorted(mem.create_summary(), reverse=True, key=itemgetter(2))[:10]:
        print(x)
    input_width = 224
    input_height = 224
    rgb_img = (img[:, :, [2, 1, 0]] * 1.0 / 255).astype(np.float32)
    lab_img = cv.cvtColor(rgb_img, cv.COLOR_RGB2Lab)
    print(1)
    l_channel = lab_img[:, :, 0]
    l_channel_resize = cv.resize(l_channel, (input_width, input_height))
    l_channel_resize -= 50
    print(1)
    Caffe_net.setInput(cv.dnn.blobFromImage(l_channel_resize))
    for x in sorted(mem.create_summary(), reverse=True, key=itemgetter(2))[:10]:
        print(x)
    ab_channel = Caffe_net.forward()[0, :, :, :].transpose((1, 2, 0))
    for x in sorted(mem.create_summary(), reverse=True, key=itemgetter(2))[:10]:
        print(x)
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
    t1 = time.time()
    total = t1-t0
    print("End colorize: "+str(total))
    for x in sorted(mem.create_summary(), reverse=True, key=itemgetter(2))[:10]:
        print(x)
    return data

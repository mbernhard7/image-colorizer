#!/usr/bin/env python
# coding: utf-8

import numpy as np
import cv2 as cv

# Load model

numpy_file = np.load('./models/pts_in_hull.npy')

Caffe_net = cv.dnn.readNetFromCaffe(
    "./models/colorization_deploy_v2.prototxt",
    "./models/colorization_release_v2.caffemodel")

# Add layers to caffe

numpy_file = numpy_file.transpose().reshape(2, 313, 1, 1)
Caffe_net.getLayer(Caffe_net.getLayerId('class8_ab')).blobs = [
    numpy_file.astype(np.float32)]
Caffe_net.getLayer(Caffe_net.getLayerId('conv8_313_rh')).blobs = [
    np.full([1, 313], 2.606, np.float32)]

# Get test image from user

while True:
    image_path = input('Full path to image (jpg or png only): ').strip()
    frame = cv.imread(image_path)
    if frame is not None:
        break
    print('Failed to load image. Try again.\n')

# extract and resize L channel

input_width = 224
input_height = 224

rgb_img = (frame[:, :, [2, 1, 0]] * 1.0 / 255).astype(np.float32)
lab_img = cv.cvtColor(rgb_img, cv.COLOR_RGB2Lab)
l_channel = lab_img[:, :, 0]

l_channel_resize = cv.resize(l_channel, (input_width, input_height))
l_channel_resize -= 50


# Predict ab channel

Caffe_net.setInput(cv.dnn.blobFromImage(l_channel_resize))
ab_channel = Caffe_net.forward()[0, :, :, :].transpose((1, 2, 0))

(original_height, original_width) = rgb_img.shape[:2]
ab_channel_us = cv.resize(ab_channel, (original_width, original_height))
lab_output = np.concatenate(
    (l_channel[:, :, np.newaxis], ab_channel_us), axis=2)
bgr_output = np.clip(cv.cvtColor(lab_output, cv.COLOR_Lab2BGR), 0, 1)
extension = image_path.split('.')[-1]
out_path = ".".join(image_path.split('.')[:-1])+"-colorized."+extension
cv.imwrite(out_path, (bgr_output*255).astype(np.uint8))
print('Outputted result to '+out_path)

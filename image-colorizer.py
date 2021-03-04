from flask import Flask, request, render_template, jsonify, send_file
from PIL import Image
import PIL.ImageOps   
from io import BytesIO
import time

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
	return render_template('main.html')

@app.route('/colorize', methods=['POST'])
def colorize():
	try:
		t0 = time.time()
		file = request.files['imageFile']
		extension=file.filename.split('.')[-1]
		img = Image.open(file.stream).convert('RGB')
		img=PIL.ImageOps.invert(img)
		img_io = BytesIO()
		img.save(img_io, extension.upper(), quality=100)
		img_io.seek(0)
		t1 = time.time()
		total = t1-t0
		if t1-t0<3:
			time.sleep(3-(t1-t0))
		return send_file(img_io, mimetype='image/'+extension.lower()), 200
	except Exception as e:
		return f"An Error Occured: {e}",400
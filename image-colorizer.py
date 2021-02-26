from flask import Flask, request, render_template, jsonify, send_file
from PIL import Image
import io
import base64

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
	return render_template('main.html')

@app.route('/colorize', methods=['POST'])
def colorize():
	try:
		file = request.files['imageFile']
		img = Image.open(file.stream)
		img_byte_arr = io.BytesIO()
    	img.save(img_byte_arr, format='PNG')
    	my_encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
		return jsonify({'msg': 'success', 'imageFile': my_encoded_img}),200
	except Exception as e:
		return f"An Error Occured: {e}",400

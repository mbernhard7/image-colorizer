from flask import Flask, request, render_template, jsonify, send_file
from PIL import Image
from io import BytesIO

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
		img_io = BytesIO()
		pil_img.save(img_io, 'JPEG', quality=70)
		img_io.seek(0)
		return send_file(img_io, mimetype='image/jpeg'), 200

	except Exception as e:
		return f"An Error Occured: {e}",400
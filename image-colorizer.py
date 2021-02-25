from flask import Flask, request, render_template, jsonify
from PIL import Image

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
		return jsonify({'msg': 'success', 'size': [img.width, img.height]})
	except Exception as e:
		return f"An Error Occured: {e}"

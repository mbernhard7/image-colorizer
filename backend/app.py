from flask import Flask, request, render_template, jsonify, make_response
from flask_cors import CORS
from image_colorizer import colorize_file
import sys
import traceback

app = Flask(__name__)
cors = CORS(app, origins=['http://127.0.0.1:8000', 'https://cs121-image-colorizer.herokuapp.com'])

@app.route('/colorize', methods=['POST'])
def colorize():
    """Receive an image, colorizes it, and  return it in base64 encoding

    Returns:
        JSON Response: contains a base64 encoding of the colorized image
    """
    try:
        file = request.files['imageFile']
        extension = file.filename.split('.')[-1]
        data = colorize_file(file, extension)
        res = make_response(jsonify(data), 200)
        return res

    except Exception as e:
        print(traceback.format_exc(), file=sys.stderr)
        res = make_response(f"An Error Occured: {traceback.format_exc()}", 400)
        res.headers['Access-Control-Allow-Origin']: '*'
        return res

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8001)
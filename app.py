from flask import Flask, request, render_template, jsonify, make_response
from image_colorizer import colorize_file


app = Flask(__name__)


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
    """Receive an image, colorizes it, and  return it in base64 encoding

    Returns:
        JSON Response: contains a base64 encoding of the colorized image
    """
    try:
        file = request.files['imageFile']
        extension = file.filename.split('.')[-1]
        data = colorize_file(file, extension)
        return make_response(jsonify(data), 200)

    except Exception as e:
        print(e)
        return f"An Error Occured: {e}", 400

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from image_colorizer import colorize_file
import sys
import traceback

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
CORS(app, origins=["http://localhost:8000",
                   "http://127.0.0.1:8000",
                   "https://cs121-image-colorizer.herokuapp.com"],
     supports_credentials=True)


@app.route('/colorize', methods=['POST'])
def colorize():
    """Receive an image, colorizes it, and  return it in base64 encoding

    Returns:
        JSON Response: contains a base64 encoding of the colorized image
    """
    try:
        file = request.files['imageFile']
        extension = file.filename.split('.')[-1]
        if not (extension.lower().replace('jpg','jpeg') in ['jpeg', 'png']):
            raise OSError("File type ."+extension+" not accepted")
        data = colorize_file(file, extension)
        res = make_response(jsonify(data), 200)
        return res
    except Exception as err:
        print(str(type(err))+": "+str(err), file=sys.stderr)
        if type(err)==OSError:
            res = make_response(str(err), 415)
        elif type(err)==TypeError:
            res = make_response("File could not be processed.", 400)
        else:
            res = make_response(str(err), 400)
        return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)

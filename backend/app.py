from flask import Flask, request, jsonify, make_response, g
from flask_cors import CORS
from image_colorizer import colorize_file
import sys
import traceback
import time
import datetime
from rfc3339 import rfc3339
import colors

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
CORS(app, origins=["http://localhost:8000",
                   "http://127.0.0.1:8000",
                   "https://cs121-image-colorizer.herokuapp.com"],
     supports_credentials=True)


@app.before_request
def before_request():
    g.start = time.time()

@app.after_request
def log_request(response):
    if request.path == '/favicon.ico':
        return response
    elif request.path.startswith('/static'):
        return response

    now = time.time()
    duration = round(now - g.start, 2)
    dt = datetime.datetime.fromtimestamp(now)
    timestamp = rfc3339(dt, utc=True)

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    host = request.host.split(':', 1)[0]
    args = dict(request.args)

    log_params = [
        ('method', request.method, 'blue'),
        ('path', request.path, 'blue'),
        ('status', response.status_code, 'yellow'),
        ('duration', duration, 'green'),
        ('time', timestamp, 'magenta'),
        ('ip', ip, 'red'),
        ('host', host, 'red'),
        ('params', args, 'blue')
    ]

    request_id = request.headers.get('X-Request-ID')
    if request_id:
        log_params.append(('request_id', request_id, 'yellow'))

    parts = []
    for name, value, color in log_params:
        part = colors.color("{}={}".format(name, value), fg=color)
        parts.append(part)
    line = " ".join(parts)

    app.logger.info(line)

    return response

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

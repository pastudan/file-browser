#!flask/bin/python
from flask import Flask, send_from_directory
import json
import os

app = Flask(__name__)


# ideally these would go behind nginx or something..
@app.route('/', defaults={'path': None})
@app.route('/static/<path:path>')
def index(path):
    if path is None:
        path = 'index.html'
    return send_from_directory('static', path)



# API
@app.route('/api/v1.0/files/', methods=['GET'], defaults={'path': ''})
@app.route('/api/v1.0/files/<path:path>', methods=['GET'])
def get_files(path):
    path = os.path.expanduser('~/'+path)
    walk = next(os.walk(path))
    items = {
        'directories': walk[1],
        'files': walk[2]
    }
    return json.dumps(items)



# download file
@app.route('/download/<path:path>')
def download(path):
    return send_from_directory(os.path.expanduser('~'), path)


if __name__ == '__main__':
    app.run(debug=True)
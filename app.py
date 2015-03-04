#!/bin/python
from flask import Flask, send_from_directory
import json
import os
import zipfile

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
    path = os.path.join(os.path.expanduser('~'), path)
    walk = next(os.walk(path))
    items = {
        'directories': walk[1],
        'files': walk[2]
    }
    return json.dumps(items)



# download file (again.. nginx would be good here..)
@app.route('/download/<path:path>')
def download(path):
    return send_from_directory(os.path.expanduser('~'), path)


# zip directory
@app.route('/zip/.zip', defaults={'path': ''})
@app.route('/zip/<path:path>.zip')
def zip(path):
    zip_path = path.replace('/','-') + '.zip'
    zipf = zipfile.ZipFile(os.path.join('/tmp', zip_path), 'w')
    zipdir(os.path.join(os.path.expanduser('~'),path), zipf)
    zipf.close()

    return send_from_directory('/tmp', zip_path)


def zipdir(path, zip):
    head_length = len(os.path.dirname(path))
    for root, dirs, files in os.walk(path):
        for file in files:
            rel_path = os.path.join(root, file)[head_length:]
            zip.write(os.path.join(root, file), rel_path, zipfile.ZIP_STORED)




if __name__ == '__main__':
    app.run(debug=True)
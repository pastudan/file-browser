#!flask/bin/python
from flask import Flask, send_from_directory
import json
from glob import glob
import os

app = Flask(__name__)


# ideally these would go behind nginx or something..
@app.route('/')
def index():
    return send_from_directory('static/', 'index.html')

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)



# API
@app.route('/browser/api/v1.0/files/', methods=['GET'], defaults={'path': ''})
@app.route('/browser/api/v1.0/files/<path:path>', methods=['GET'])
def get_files(path):
    path = os.path.expanduser('~/'+path+'/*')
    print path
    return json.dumps(glob(path))

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask
from flask import request
import json

import request

app = Flask(__name__)

# json 파일을 연다.

with open('example_return.json') as json_file:
    json_data = json.load(json_file)


@app.route('/')
def index():
    return json_data["lastUpdate"]


@app.route('/api/highlight/<url>')
def highlight(url):
    # json 데이터 중 원하는 부분 찾아서 그 부분만 return
    for data in json_data:
        if data["videoId"] == url:
            return data
    return "none"


@app.route('/info')
def info():
    return 'Info'

# -*- coding: utf-8 -*-
# 파이썬 버젼에 따른 인코딩 문제 때문에 줄 추가

from flask import Flask, jsonify, request
import json
from flask_cors import CORS
from flask_restful import Resource, Api
import sys
from ast import literal_eval

sys.path.append("../")
from data_processing import data_processing
from comment_highlight import comment_highlight

app = Flask(__name__)
api = Api(app)
CORS(app)
# json 파일을 연다.

with open('../data/result.json') as json_file:
    json_data = json.load(json_file)


@app.route('/')
def index():
    return json_data


@app.route('/api/highlight/<url>')
def highlight(url):
    # json 데이터 중 원하는 부분 찾아서 그 부분만 return
    for data in json_data:
        if data["videoId"] == url:
            return data
    return "none"


# json 파일을 받은 후 그대로 return 하는 함수
@app.route('/api/echo-json', methods=['GET', 'POST', 'DELETE', 'PUT'])
def add():
    data = request.get_json()
    # ... do your business logic, and return some response
    # e.g. below we're just echo-ing back the received JSON data
    return jsonify(data)


@app.route('/info')
def info():
    return "hello"


@app.route('/predict', methods=['POST'])
def predict():
    return jsonify({'class_id': 'IMAGE_NET_XXX', 'class_name': 'Cat'})


@app.route('/post', methods=['POST', 'GET'])
def post():
    print("Loaded")
    print(json.loads(request.get_data()))
    data = json.loads(request.get_data())
    data = json.dumps(data, ensure_ascii=False).encode('utf8')
    # binary data를 string으로 변환
    data = eval(data)
    # 현재 받은 data에서는 true, false라고 저장되어 있는데 python에서는 True, False라고 저장해야한다
    data = data.replace("true", "True")
    data = data.replace("false", "False")
    # string to dictionary
    data = literal_eval(data)
    # 데이터 1차 가공 - input 데이터 중 댓글만 받는다
    data2 = data_processing(data)
    # 가공된 데이터는 string 형이라, 다시 dictionary 형태로 변환
    data2 = literal_eval(data2)
    # 데이터 2차 가공 - highlighting
    data3 = comment_highlight(data2)
    return jsonify(data3)


# host 주소는 0.0.0.0, 3000번 포트에서 배포
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000', debug=True)

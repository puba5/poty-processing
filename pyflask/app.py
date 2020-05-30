from flask import Flask, jsonify
import json
from flask_cors import CORS
from flask_restful import Resource, Api

import request

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
    value = request.form['test']
    return value


class CreateUser(Resource):
    def post(self):
        print(self)
        return {'status': 'success'}


api.add_resource(CreateUser, '/user')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000', debug=True)

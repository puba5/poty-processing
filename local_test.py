from data_processing import data_processing
from comment_highlight import comment_highlight
import json

# 로컬에서 테스트를 위한 코드
# 테스트할 .json 파일의 이름을 입력
# 파일은 data 폴더 내에 .json 파일로 있어야함

file_name = input()

with open('./data/' + file_name + '.json') as json_file:
    json_data = json.load(json_file)

    new_json_data = data_processing(json_data, file_name)
    print(new_json_data)
    json_file.close()

with open('./data/' + file_name + '_output_dummy.json') as json_file:
    json_data = json.load(json_file)
    comment_highlight(json_data, file_name)

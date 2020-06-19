from data_processing import data_processing_local
from comment_highlight import comment_highlight_local
import json

file_name = input()

with open('./data/' + file_name + '.json') as json_file:
    json_data = json.load(json_file)

    new_json_data = data_processing_local(json_data, file_name)
    print(new_json_data)
    json_file.close()

with open('./data/' + file_name + '_output_dummy.json') as json_file:
    json_data = json.load(json_file)
    comment_highlight_local(json_data, file_name)

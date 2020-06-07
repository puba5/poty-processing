import json
import re
from collections import OrderedDict

# Youtube API로부터 받은 데이터 파일을 가공하여 프론트에 표시될 수 있게 가공한다
# 현재 결과는 output_dummy.json 파일로 생성한다

tmp = './data/input_dummy.json'


def data_processing(input_json):
    # with open('./data/input_dummy.json') as json_file:
    # json 파일을 불러온다
    # json_data = json.load(input_json)
    json_data = input_json

    processed_video_data = OrderedDict()
    video_id = json_data["items"][0]["snippet"]["videoId"]
    processed_video_data["video_id"] = video_id
    # 받은 댓글의 수
    commnet_all_cnt = json_data["pageInfo"]["totalResults"]
    # 받은 댓글의 수를 저장해준다
    processed_video_data["totalResults"] = commnet_all_cnt

    processed_comment_list = []

    for comment_number in range(commnet_all_cnt):
        # 필요한 정보들을 불러온다
        video_id = json_data["items"][comment_number]["snippet"]["videoId"]
        # 댓글 내용
        text_display = json_data["items"][comment_number]["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        # print(text_display)
        # 좋아요 수
        like_count = json_data["items"][comment_number]["snippet"]["topLevelComment"]["snippet"]["likeCount"]
        # 댓글 작성자
        user_id = json_data["items"][comment_number]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        # total_reply_count
        totalReplyCount = json_data["items"][comment_number]["snippet"]["totalReplyCount"]
        # 댓글 작성 시간
        # published_at

        # 시간을 정규 표현식을 이용하여 구한다
        # 시간, 즉 timestamp는 4가지 경우

        time_stamp_list = []
        # time case 1 : 10분 미만 ex) 3:32
        time_case_1 = re.compile(r'\d:\d\d')
        time_stamp_list.extend(time_case_1.findall(text_display))
        # time case 2 : 1시간 미만 ex) 35:53
        time_case_2 = re.compile(r'\d\d:\d\d')
        time_stamp_list.extend(time_case_2.findall(text_display))
        # time case 3 : 10시간 미만 ex) 1:32:34
        time_case_3 = re.compile(r'\d:\d\d:\d\d')
        time_stamp_list.extend(time_case_3.findall(text_display))
        # time case 4 : 100시간 미만 ex) 11:23:53
        time_case_4 = re.compile(r'\d\d:\d\d:\d\d')
        time_stamp_list.extend(time_case_4.findall(text_display))
        # 추후 타임스탬프 댓글을 읽기 위해서는 아래 코드 사용
        # Regex span , regex group span
        # if time_case_1.findall(text_display):
        #     print(time_case_1.search(text_display).span(0))

        processed_comment = OrderedDict()
        processed_comment["video_id"] = video_id
        processed_comment["text_display"] = text_display
        processed_comment["like_count"] = like_count
        processed_comment["time_stamp"] = time_stamp_list
        processed_comment["user_id"] = user_id
        processed_comment["totalReplyCount"] = totalReplyCount

        processed_comment_list.append(processed_comment)

    processed_video_data["comments"] = processed_comment_list

    # with open("./data/output_dummy.json", "w", encoding="utf-8") as fp:
    #     json.dump(processed_video_data, fp, ensure_ascii=False, indent="\t")

    return json.dumps(processed_video_data, ensure_ascii=False, indent="\t")


# 파일에 작성하여 테스트

# with open('./data/input_dummy.json') as json_file:
#     json_data = json.load(json_file)
#
#     new_json_data = data_processing(json_data)
#     print(new_json_data)

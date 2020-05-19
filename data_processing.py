import json
import re
from collections import OrderedDict

# Youtube API로부터 받은 데이터 파일을 가공하여 프론트에 표시될 수 있게 가공한다
# 현재 결과는 output_dummy.json 파일로 생성한다

with open('./data/input_dummy.json') as json_file:
    # json 파일을 불러온다
    json_data = json.load(json_file)
    # 댓글 번호
    processed_video_data = OrderedDict()
    video_id = json_data["items"][0]["snippet"]["videoId"]
    processed_video_data["video_id"] = video_id
    processed_comment_list = []
    for comment_number in range(100):
        # 필요한 정보들을 불러온다
        video_id = json_data["items"][comment_number]["snippet"]["videoId"]
        # 댓글 내용
        text_display = json_data["items"][comment_number]["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        print(text_display)
        # 좋아요 수
        like_count = json_data["items"][comment_number]["snippet"]["topLevelComment"]["snippet"]["likeCount"]
        # user_id
        # 댓글 작성 시간
        # published_at
        # 전체 대댓글 개수
        # total_reply_count

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

        processed_comment = OrderedDict()
        processed_comment["video_id"] = video_id
        processed_comment["text_display"] = text_display
        processed_comment["like_count"] = like_count
        processed_comment["time_stamp"] = time_stamp_list

        processed_comment_list.append(processed_comment)

    processed_video_data["comments"] = processed_comment_list

    with open("./data/output_dummy.json", "w", encoding="utf-8") as fp:
        json.dump(processed_video_data, fp, ensure_ascii=False, indent="\t")

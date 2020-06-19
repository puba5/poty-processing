# -*- coding: utf-8 -*-
import json
import operator
from collections import OrderedDict


# 3:55 같은 string 형태의 시간을 초단위의 int형으로 변환하는 함수
# 정수형으로 변경해주어 시간을 비교할 수 있도록 한다.

def time_conversion(time_string):
    hour = 0
    minute = 0
    sec = 0
    # time case 1 : 10분 미만 ex) 3:32
    if len(time_string) == 4:
        minute = int(time_string[0:1])
        sec = int(time_string[3:])
    # time case 2 : 1시간 미만 ex) 35:53
    if len(time_string) == 5:
        minute = int(time_string[0:2])
        sec = int(time_string[3:])
    # time case 3 : 10시간 미만 ex) 1:32:34
    if len(time_string) == 7:
        hour = int(time_string[0:1])
        minute = int(time_string[2:4])
        sec = int(time_string[5:])
    # time case 4 : 100시간 미만 ex) 11:23:53
    if len(time_string) == 8:
        hour = int(time_string[0:2])
        minute = int(time_string[3:5])
        sec = int(time_string[6:])
    time_num = 60 * 60 * hour + 60 * minute + sec
    return time_num


def comment_highlight(json_file, file_name=""):
    json_data = json_file
    # 처리된 결과를 저장할 json Data

    processed_highlight_data = OrderedDict()

    video_id = json_data["video_id"]
    processed_highlight_data["videoId"] = video_id
    processed_highlight_data["lastUpdate"] = ""

    processed_highlight_list = []

    highlight_list = dict()

    # comment 개수
    comment_all_cnt = json_data["totalResults"]

    # 연 json 파일을 저장한다
    data_list = []

    for i in range(comment_all_cnt):
        text_display = json_data["comments"][i]['text_display']
        time_stamps = json_data["comments"][i]['time_stamp']
        like_count = json_data["comments"][i]['like_count']
        reply_count = json_data["comments"][i]['totalReplyCount']

        # 연 json 파일을 저장한다.
        data_list.append({"text_display": json_data["comments"][i]['text_display'],
                          "time_stamps": json_data["comments"][i]['time_stamp'],
                          "like_count": json_data["comments"][i]['like_count'],
                          "user_id": json_data["comments"][i]['user_id'],
                          "totalReplyCount": json_data["comments"][i]['totalReplyCount']})

        for time_stamp in time_stamps:
            if time_stamp in highlight_list:
                highlight_list[time_stamp][0] += like_count
                highlight_list[time_stamp][1] += reply_count
            else:
                highlight_list[time_stamp] = [like_count, reply_count]
                # highlight_list_replyCnt[time_stamp] = reply_count

    b = sorted(highlight_list.items())
    # 좋아요 수로 정렬하여 가장 높은 하이라이트를 구한다
    highlight_by_likecount = sorted(highlight_list.items(), reverse=True, key=operator.itemgetter(1))

    print(highlight_by_likecount)
    # 하이라이트로 보여줄 개수
    highlight_cnt = 5
    # 댓글의 개수가 보여줄 하이라이트의 개수보다 적을 수도 있으므로, 전체 댓글 개수와 보여줄 하이라이트 개수 중 작은 값을 채택

    for k in range(min(highlight_cnt, comment_all_cnt)):
        highlight = OrderedDict()
        highlight["rank"] = k + 1
        highlight["timestamp"] = highlight_by_likecount[k][0]
        highlight["totalLikeCount"] = highlight_by_likecount[k][1][0]
        highlight["totalReplyComment"] = highlight_by_likecount[k][1][1]

        # 이전 하이라이트와 겹치는지 확인
        isDup = False
        for l in range(k):
            # 하이라이트들의 시간과 현재 보는 댓글의 시간 차이
            time_gap = time_conversion(processed_highlight_list[l]["timestamp"]) - time_conversion(
                highlight["timestamp"])
            # 만약 그 시간 차가 3 이하라면 같은 댓글로 취급
            if abs(time_gap) <= 3:
                # print(highlight["timestamp"], "dup")
                isDup = True

        # if isDup:
        #     highlight_cnt += 1
        #     # print("dup")

        # print("notDup")

        processed_highlight_list.append(highlight)

        highlight_comment_list = []
        for data in data_list:
            if highlight["timestamp"] in data["time_stamps"]:
                highlight_comment_info = OrderedDict()
                highlight_comment_info["commentText"] = data["text_display"]
                highlight_comment_info["likeCount"] = data["like_count"]
                highlight_comment_info["userId"] = data["user_id"]
                highlight_comment_info["replyComment"] = data["totalReplyCount"]
                highlight_comment_list.append(highlight_comment_info)
        highlight["comments"] = highlight_comment_list

    processed_highlight_data["highlights"] = processed_highlight_list

    # 만약 local 파일에 있다면, file_name에 인자를 넣어준다.
    # 그리고 결과를 result.json에 저장
    if file_name != "":
        with open("./data/" + file_name + "_result.json", "w", encoding="utf-8") as fp:
            json.dump(processed_highlight_data, fp, ensure_ascii=False, indent="\t")
    return json.dumps(processed_highlight_data)

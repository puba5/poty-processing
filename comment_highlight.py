import json
import operator
from collections import OrderedDict

with open('./data/output_dummy.json') as json_file:
    # json 파일을 불러온다
    json_data = json.load(json_file)
    # 처리된 결과를 저장할 json Data

    processed_highlight_data = OrderedDict()

    video_id = json_data["video_id"]
    processed_highlight_data["videoId"] = video_id
    processed_highlight_data["lastUpdate"] = ""

    processed_highlight_list = []

    highlight_list = dict()

    # 연 json 파일을 저장한다
    data_list = []

    for i in range(100):
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

    highlight_by_likecount = sorted(highlight_list.items(), reverse=True, key=operator.itemgetter(1))

    # 하이라이트로 보여줄 개수
    highlight_cnt = 5
    for k in range(highlight_cnt):
        highlight = OrderedDict()
        highlight["rank"] = k + 1
        highlight["timestamp"] = highlight_by_likecount[k][0]
        highlight["totalLikeCount"] = highlight_by_likecount[k][1][0]
        highlight["totalReplyComment"] = highlight_by_likecount[k][1][1]

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

    with open("./data/result.json", "w", encoding="utf-8") as fp:
        json.dump(processed_highlight_data, fp, ensure_ascii=False, indent="\t")

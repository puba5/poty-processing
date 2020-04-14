import requests
from bs4 import BeautifulSoup
from selenium import webdriver as wd
import time

# 백앤드 완전히 구현 전, 테스트를 위하여 유튜브 댓글 크롤러를 만든다.

VideoUrl = "https://www.youtube.com/watch?v=ahEMgBSxawo"
res = requests.get(VideoUrl)

# html 페이지 파싱해서 영상 제목 가져옴
soup = BeautifulSoup(res.content, 'html.parser')
title = soup.find('title')

# 찾는 영상 제목 확인
print(title.get_text())

# https://somjang.tistory.com/45의 유튜브 크롤러를 활용

# 크롬 드라이버를 따로 설치하여 폴더 내 저장하여 그것을 실행
driver = wd.Chrome('driver/chromedriver')
# 창 크기 고정
driver.set_window_size(700, 700)

# 내가 원하는 영상 비디오를 킨다.
driver.get(VideoUrl)

# 유튜브 댓글은 스크롤링하지 않으면 뜨지 않기 때문에 끝까지 스크롤링하여 댓글이 뜨도록한다.

last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
print("유튜브 댓글 스크롤링 시작")
while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    # 인터넷 느릴 경우 대비하여 4초로 수정
    time.sleep(4.0)
    new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

    if new_page_height == last_page_height:
        break
    last_page_height = new_page_height

html_source = driver.page_source
driver.close()

soup = BeautifulSoup(html_source, 'lxml')
# soup = BeautifulSoup(res.content, 'html.parser')

# 아이디와 내용을 가져온다.
# 더 세분화하여 댓글 시간과 댓글 내용을 분리할 예
youtube_user_IDs = soup.select('div#header-author > a > span')
youtube_comments = soup.select('yt-formatted-string#content-text')

str_youtube_userIDs = []
str_youtube_comments = []
for i in range(len(youtube_user_IDs)):
    str_id = str(youtube_user_IDs[i].text)  # print(str_tmp)
    str_id = str_id.replace('\n', '')
    str_id = str_id.replace('\t', '')
    str_id = str_id.replace(' ', '')
    str_youtube_userIDs.append(str_id)
    str_comment = str(youtube_comments[i].text)
    str_comment = str_comment.replace('\n', '')
    str_comment = str_comment.replace('\t', '')
    str_comment = str_comment.replace(' ', '')
    str_youtube_comments.append(str_comment)

for i in range(len(str_youtube_userIDs)):
    print(str_youtube_userIDs[i], str_youtube_comments[i])

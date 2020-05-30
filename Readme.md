# 졸업프로젝트 POTY (Play Of The Youtube)

> Find Highlight part with Youtube comments

## Clustering with Python

> python version : python 3.7

## CommentCollector

> chromedriver, lxml, beautifulSoap4 사용

## 구현 방법


## 실행 방법

> pip3 install flask <br>
> pip3 install flask-cors <br>
> pip3 install flask_restful <br>
> pip3 install request <br>
> python app.py

## 구동 과정 

> data_procssing.py : youtube API에서 가져온 raw data 중 댓글 데이터만 추출<br>
> input_dummy.json --> output_dummy.json <br>
> comment_highlight.py : 댓글 중에 하이라이트들을 선 <br> 
> output_dummy.json --> result.json <br>
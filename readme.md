SSAFY Chat Bot
=============
예약기능이 있는 챗봇
SSAFY 교육기간 중 2018년 12월 말에 3일간 진행된 프로젝트
* * *
주제 선정
-------------
* 일정한 주기마다 나는 특정 정보를 물어본다.
* 챗봇은 내가 원하는 정보를 직접 물어봐야 대답을 해준다.
* 위의 2가지를 조합하여 계속 질문을 안하더라도 먼저 대답해주는 챗봇을만들고 싶었다.


###필요한 기능

* 무엇을 크롤링 할지에 대해서 크롤링하는 정보의 종류가 필요함(날씨정보,교통정보)
* 날짜를 입력 받을 수 있어야함.
* 주기를 입력 받아야 함(매일, 한번, 주말, 특정 날, 공휴일등.)
* 예약 취소 변경이 가능하여야 한다.


* * *
완성된 기능
-------------
* 날짜와 정보, 주기를 대화를 통하여 입력 받아 예약이 가능함
* 입력된 예약에 한해서만 취소가 가능함.


* * *
구조 
-------------
![Alt text](./Gujo.PNG)
* 먼저 입력을 받고 원하는 키워드인지 판별한다
* 키워드가 예약이라면 무엇을 예약할건지 물어본다.
* 대화를 통하여 시간/주기를 설정하고, 입력이 이상할 경우 한번의 재입력이 가능하다.
* 예약종료를 입력하면 정해진 예약을 종료를 실행하는 쓰레드를 종료시킨다.


* * *
개발 환경 
-------------
* Python, Slack, Git,elice





# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request
import threading
from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template
from datetime import datetime

from datetime import datetime, timezone
from pytz import timezone

now = datetime.now()

app = Flask(__name__)

slack_token = "xoxb-503049869125-507697993413-lWHSaNxNhcyEv5bp9bH4vByB"
slack_client_id = "503049869125.507327792692"
slack_client_secret = "4e610caef78945a08b771c2622c70a05"
slack_verification = "r4EVKUMluZIUM1NxMyNfxty7"
sc = SlackClient(slack_token)

state = 0  # {0예약  / 1무엇 / 2언제 / 3주기}
state2 = 0  # { 0취소 / 1무엇}
string = ""
num = 0

thread_list = {}


# 크롤링 함수 구현하기
def _crawl_naver_keywords(text):
    results = []

    if "날씨" in text:
        url = "https://weather.naver.com/rgn/cityWetrCity.nhn?cityRgnCd=CT007004"
        req = urllib.request.Request(url)
        sourcecode = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(sourcecode, "html.parser")
        for data in soup.find("div", class_="w_now2").find_all("div", class_="fl"):
            results.append(data.find("em").get_text())
    elif "미세먼지" in text:
        url = "https://weather.naver.com/rgn/cityWetrCity.nhn?cityRgnCd=CT007004"
        req = urllib.request.Request(url)
        sourcecode = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(sourcecode, "html.parser")
        for data in soup.find("div", class_="w_now2").find_all("div", class_="fl"):
            results.append(data.find("p").get_text())

        # url = "https://movie.naver.com/movie/point/af/list.nhn"
        # #         req = urllib.request.Request(url)
        #
        # #         sourcecode = urllib.request.urlopen(url).read()
        # #         soup = BeautifulSoup(sourcecode, "html.parser")
        #
        # #         for data in (soup.find("table", class_="list_netizen").find_all("tbody")):
        # #             for dat in data.find_all("tr"):
        # #                 satiss.append(dat.find("td",class_="point").get_text())
        # #                 names.append(dat.find("a",class_="movie").get_text())
        # #                 reviews.append(dat.find("td",class_="title").get_text())

    return u'\n'.join(results)


def execute(string, channel):
    """    Execute Function on Thread
    """
    global thread_list

    Input_time = str(string).split("/")[2].split(":")[0] + ":" + str(string).split("/")[2].split(":")[1]
    frequency = str(string).split("/")[3]

    now = datetime.now()
    now_kor = datetime.now(timezone('Asia/Seoul'))
    print(now_kor)

    if frequency == "매일":
        sins = True
        while thread_list[string]:
            now = datetime.now()
            now_kor = datetime.now(timezone('Asia/Seoul'))
            delta_time = str(now_kor).split(" ")[1].split(":")[0] + ":" + str(now_kor).split(" ")[1].split(":")[1]
            if (Input_time == delta_time and sins):
                results = _crawl_naver_keywords(string)
                if "날씨" in string:
                    strin1 = ""
                    for result in results:
                        if (result != " " and result != "\t" and result != "\n"):
                            strin1 = strin1 + result
                    results = strin1
                else:
                    strin1 = ""
                    for result in results:
                        if (result != " " and result != "\t" and result != "\n" and result != "|"):
                            strin1 = strin1 + result
                    results = strin1.replace("도움말", "")

                # print(results)
                sc.api_call(
                    "chat.postMessage",
                    channel=channel,
                    text=str(now_kor).split(" ")[0] + results  # text_
                )
                sins = False
            elif Input_time != delta_time and not sins:
                sins = True
    elif frequency == "한번":
        while thread_list[string]:
            now = datetime.now()
            now_kor = datetime.now(timezone('Asia/Seoul'))
            delta_time = str(now_kor).split(" ")[1].split(":")[0] + ":" + str(now_kor).split(" ")[1].split(":")[1]

            if (Input_time == delta_time):
                results = _crawl_naver_keywords(string)
                if "날씨" in string:
                    strin1 = ""
                    for result in results:
                        if (result != " " and result != "\t" and result != "\n"):
                            strin1 = strin1 + result
                    results = strin1
                else:
                    strin1 = ""
                    for result in results:
                        if (result != " " and result != "\t" and result != "\n" and result != "|"):
                            strin1 = strin1 + result
                    results = strin1.replace("도움말", "")

                    results = strin1
                sc.api_call(
                    "chat.postMessage",
                    channel=channel,
                    text=str(now_kor).split(" ")[0] + results  # text_
                )
                break


# 이벤트 핸들하는 함수

def _text_exac(text):
    arr = text.split(":")

    if 0 <= int(arr[0]) and int(arr[0]) <= 23 and 0 <= int(arr[1]) and int(arr[1]) <= 59:
        return True
    return False


def delete_text_exac(text):
    global thread_list
    if thread_list[text] != "":
        return True
    return False


def _event_handler(event_type, slack_event):
    global state
    global state2
    global num
    global string
    global thread_list


    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]
        text_ = "-"

        arr = text.split(" ")

        if len(arr) == 5:
            text_ = "'예약' 기능이 있습니다\n예약기능을 사용해 보세요"
        else:
            text = text.split(" ")[1].replace("\n", "")
            if state > 0:
                if state == 1 and ("1" == text or "2" == text):
                    text_ = "몇시에 예약을 하시겠습니까? (시:분) 형태로 입력"
                    state = 2
                    num = 0
                    if "1" in text:
                        string = string + "/날씨"
                    else:
                        string = string + "/미세먼지"

                elif state == 2 and (_text_exac(text)):
                    text_ = "주기를 어떻게 설정하시겠습니까?\n1 : 매일\n2 : 한번"  # \n3 : 한번"
                    state = 3
                    num = 0
                    string = string + "/" + text
                elif state == 3 and ("1" == text or "2" == text):  # or "3" == text):
                    if "1" in text:
                        string = string + "/매일"
                    elif "2" in text:
                        string = string + "/한번"
                    # else:
                    #     string = string + "/한번"
                    thread_list[string] = True
                    my_thread = threading.Thread(target=execute, args=(string, channel))
                    my_thread.start()

                    text_ = string
                    string = ""
                    state = 0
                    num = 0
                elif num < 1:
                    text_ = "다시 입력하십시오"
                    num = num + 1
                else:
                    text_ = "오 입력으로 예약을 종료합니다"
                    state = 0
                    string = ""
                    num = 0
            elif state == 0 and "예약" == text:
                text_ = "무엇을 예약하시겠습니까?\n1 : 날씨\n2 : 미세먼지"
                state = 1
                string = string + "예약완료"
                num = 0
            elif state2 == 1 and delete_text_exac(text):
                text_ = "삭제 완료"
                state2 = 0
                thread_list[text] = False
            elif "예약종료" == text and state2 == 0:
                text_ = "예약 종료할 예약명을 입력하세요( 예약완료/종료/시간/주기 )"
                state2 = 1
            else:
                text_ = "오 입력입니다"
                state = 0
                state2 = 0
                string = ""
                num = 0

        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=text_  # text_
        )

        return make_response("App mention message has been sent", 200, )

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)


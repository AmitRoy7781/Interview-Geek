from _datetime import datetime,timedelta
from bs4 import BeautifulSoup
import requests,json,urllib
from flask import render_template, request, redirect, session, Blueprint

app = Blueprint('contestReminder', __name__)

@app.route("/contest_reminder")
def upcoming_contests():

    # print("amit")

    url = "https://clist.by:443/api/v1/contest/?end__gt="
    stTime = datetime.today() - timedelta(hours=6, minutes=0)
    enTime = datetime.today() - timedelta(hours=6, minutes=0) + timedelta(hours=480, minutes=0)

    begin = str(stTime.year) + "-" + str(stTime.month) + "-" + str(stTime.day) + "T" + str(stTime.hour) + "%3A" + str(stTime.minute) + "%3A" + str(stTime.second)
    endd = str(enTime.year) + "-" + str(enTime.month) + "-" + str(enTime.day) + "T" + str(enTime.hour) + "%3A" + str(enTime.minute) + "%3A" + str(enTime.second)
    # print(begin)
    # print(endd)
    url3 = "https://clist.by:443/api/v1/contest/?end__gt=" + begin + "&" + "end__lt=" + endd

    # print(url3)
    # print(url)
    res = requests.get(url3,headers={'Authorization': 'ApiKey Ahb_arif:e746f33d1dca698bf9e578774d86dafb916fe288'})
    # print(res.text)
    jsonData = res.json()
    objects = jsonData["objects"]
    contestData = []
    for x in objects:

        siteName = x["resource"]["name"]
        contestName = x["event"]
        startTime = str(x["start"])
        startTime.replace("T", " , ")
        endTime = str(x["end"])
        endTime.replace("T", " , ")
        link = x["href"]
        duration = int(float(x["duration"]) * 0.000277778)

        if duration >=24:
            d = int(duration/24)
            h = duration % 24
            duration = str(d) + " days "
            if h >0:
                duration+= str(h) + " hours "

        else:
            duration = str(duration) + " hours"

        if siteName == "codeforces.com" or siteName == "csacademy.com" or siteName == "hackerrank.com" or siteName=="codechef.com":
            temp = {}
            temp["sitename"] = siteName
            temp["contest_name"] = contestName
            temp["startTime"] = startTime.replace("T",", ") +" (GMT)"
            temp["endTime"] = endTime.replace("T",", ") +" (GMT)"
            temp["link"] = link
            temp["duration"] = duration

            contestData.append(temp)
            print(x)


    return render_template('/contestReminder/Upcoming Contests.html',contestInfo=contestData)

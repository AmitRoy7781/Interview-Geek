from flask import render_template, request, redirect, session, Blueprint, json
from iGeekAuth.auth import signin
from bs4 import BeautifulSoup
import requests
import copy
import datetime
from iGeekFirebase.firebase import firebase
import datetime

db = firebase.database()

app = Blueprint('blog', __name__)

@app.route('/blog/')
def showBlog():
    prototype = Prototype()
    prototype_copy = copy.deepcopy(prototype)
    return prototype_copy.show_blog()


class Prototype:
    """
    Example class to be copied.
    """

    def show_blog(self):

        if 'username' not in session.keys():
            return signin(None, "/blog/")


        blog_data = db.child("Blogs").get().val()
        data = []
        message = []

        for blog in blog_data.keys():
            data.append(blog_data[blog])



        for item in data:
            tmp = []
            tmp.append(item["title"])
            tmp.append(item["author"])
            # tmp.append("Author Nai")
            tmp.append(item["date"])
            imgurl = item["imgurl"].split(" ")
            tmp.append(imgurl)
            print(imgurl)

            tmp.append(item["content"])

            message.append(tmp)

            # print(tmp[0]+" "+tmp[1]+" "+tmp[2]+" "+tmp[3])

        message.sort(key=lambda message: message[2])
        message.reverse()

        return render_template("/blog/show_blog.html", blog_data=message)


@app.route('/blog/add/', methods=['GET', 'POST'])
def add():

    if 'username' not in session.keys():
        return signin(None,"/blog/")

    if request.method == 'POST':
        title = request.form['title']
        htmlcontent = request.form['imagecontent']

        if title == "" or htmlcontent == "":
            return redirect('/blog/')
        else:
            blog_message = {}
            blog_message["author"] = session['username']
            blog_message["title"] = title

            soup = BeautifulSoup(str(htmlcontent),'lxml')

            content = ""
            paragraph = soup.find_all("p")

            for i in range(1,len(paragraph)):

                para=paragraph[i]
                content += str(para.text)
                content += " "

            blog_message["content"] = content

            imgurl = soup.find_all("img")

            if imgurl != None:
                blog_message["imgurl"] = ""
                first = False
                for images in imgurl:
                    if first == True:
                        blog_message["imgurl"] += " "
                    blog_message["imgurl"]+=images["src"]
                    first = True
            else:
                blog_message["imgurl"] = ""



            current_utc_time = datetime.datetime.utcnow()
            time_delta = datetime.timedelta(hours=6)
            current_bd_time = current_utc_time + time_delta
            current_bd_time = current_bd_time.strftime('%Y-%m-%d %H:%M:%S')
            # print(current_bd_time)

            blog_message["date"] = str(current_bd_time)

            print(blog_message)
            db.child("Blogs").push(blog_message)

            return redirect('/blog/')

    else:
        return render_template("/blog.html")
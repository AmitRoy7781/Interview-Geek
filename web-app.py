from flask import Flask,render_template
import os


from iGeekAuth.auth import app as auth
from iGeekContestReminder.contestReminder import app as contestReminder
from iGeekChat.Chat import app as chat
from iGeekBlog.blog import app as blog
from iGeekProfile.profile import app as profile
from iGeekInterviewPlatform.interview_platform import app as interviewplatform


app = Flask(__name__)
app.secret_key = 'NeverEverGiveUp'


# authentication blueprint
app.register_blueprint(auth)

# contestReminder blueprint
app.register_blueprint(contestReminder)

# chat blueprint
app.register_blueprint(chat)

#blog blueprint
app.register_blueprint(blog)

#blog blueprint
app.register_blueprint(profile)

#interview platform blueprint
app.register_blueprint(interviewplatform)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/p2pchatting')
def video_chat():
    return render_template("videoChat.html")

@app.route('/screenSharing')
def screen_share():
    return render_template("screenSharing.html")

@app.route('/onlineIDE')
def online_ide():
    return render_template("onlineide.html")



if __name__ == '__main__':
    app.run(port=8000,debug=True)

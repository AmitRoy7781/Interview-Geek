from flask import Flask,render_template
import os

app = Flask(__name__)


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
def onlineIDE():
    return render_template("onlineIDE.html")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=8000)

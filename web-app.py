from flask import Flask,render_template

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



if __name__ == '__main__':
    app.run(port=8000,debug=True)

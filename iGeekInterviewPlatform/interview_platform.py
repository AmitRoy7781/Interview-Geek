from flask import render_template, request, jsonify, redirect, session, Blueprint, json
from iGeekAuth.auth import signin
from bs4 import BeautifulSoup
import requests
import copy
import datetime
from iGeekFirebase.firebase import firebase
import datetime
import string
from passlib.hash import sha256_crypt
import pusher


db = firebase.database()
auth = firebase.auth()

db = firebase.database()

app = Blueprint('interview_platform', __name__)


pusher_client = pusher.Pusher(
  app_id='630604',
  key='76e1eff5e36b22e9f0ef',
  secret='a583aa33cdf7b65a5d07',
  cluster='ap2',
  ssl=True
)


@app.route('/interview_platform/')
def interview_platform():

    if 'username' not in session.keys():
        return signin(None, "/interview_platform/")

    return render_template("/interviewPlatform/interviewplatform2.html")


#
# @app.route('/chat-room2/')
# def index():
#     messages = db.chat.find()
#
#     return render_template('temp.html', messages=messages)


@app.route('/mymessage', methods=['POST'])
def message():
    if 'username' not in session.keys():
        return signin(None, "/interview_platform/")

    # print(request.form.to_dict())
    try:

        author =request.form.get('author')
        msg = request.form.get('data')
        language = request.form.get('language')
        input = request.form.get('input')
        output = request.form.get('output')

        # print(author, " ", message)

        pusher_client.trigger('my-channel', 'new-message', {'author': author,'data': msg,
        'language':language,'input':input,'output':output})

        return render_template('/interviewPlatform/interviewplatform2.html')

    except:

        return jsonify({'result': 'failure'})
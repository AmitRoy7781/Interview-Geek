from flask import render_template, request, redirect, session, Blueprint, json
from iGeekAuth.auth import signin
from bs4 import BeautifulSoup
import requests
import copy
import datetime
from iGeekFirebase.firebase import firebase
import datetime

db = firebase.database()

app = Blueprint('profile', __name__)

@app.route('/profile/')
def showProfile():
    return render_template("/profile/profile.html")

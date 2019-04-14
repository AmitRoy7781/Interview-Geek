import pyrebase
from flask import *

config = {
    "apiKey": "AIzaSyCCCUG-t-VMgg9GIhxzIflUbuMx3Cz44mk",
    "authDomain": "interview-geek.firebaseapp.com",
    "databaseURL": "https://interview-geek.firebaseio.com",
    "projectId": "interview-geek",
    "storageBucket": "interview-geek.appspot.com",
    "messagingSenderId": "408912129017"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()


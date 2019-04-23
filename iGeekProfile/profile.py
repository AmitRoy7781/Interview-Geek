from flask import render_template, request, redirect, session, Blueprint, json
from iGeekAuth.auth import signin
from bs4 import BeautifulSoup
import requests
import copy
import datetime
from iGeekFirebase.firebase import firebase
import datetime
import string
from passlib.hash import sha256_crypt

db = firebase.database()
auth = firebase.auth()

db = firebase.database()

app = Blueprint('profile', __name__)

@app.route('/profile/')
def showProfile():
    data = db.child("Users").child(str(session['uid'])).get().val()
    # print(data)
    user_data = {}
    for x in data:
        user_data[x] = data[x]
    print(user_data)
    return render_template("/profile/profile.html",user_data=user_data)


@app.route('/edit_profile/', methods=['POST', 'GET'])
def editProfile():
    if request.method == 'POST':
        data = request.form.to_dict()

        print(data)

        name = data['name']
        # username = data['username']
        # email = data['email']
        phone_number = data['phone_number']
        password = data['password']
        c_password = data['c_password']

        address = data['address']
        dob = data['dob']
        cf = data['cf_handle']
        topcoder = data['topcoder_handle']
        hackerrank = data['hackerrank_handle']
        codechef = data['codechef_handle']
        uhunt = data['uhunt_handle']

        github = data['github']
        linkedin = data['linkedin']


        flag = True

        if len(name) < 6:
            flag = False
            data['name_msg'] = 'Name must be atleast 6 characters.'

        for ch in name:
            if ch not in string.ascii_letters and ch != ' ':
                flag = False
                data['name_msg'] = 'Name can contain [a-z][A-Z] and whitespace only.'

        # if len(username) < 6:
        #     flag = False
        #     data['username_msg'] = 'Username must be atleast 6 characters.'

        user_data = db.child("Users").get().val()
        users = []

        for user in user_data:
            users.append(user_data[user])

        # for user in users:
        #     if user["username"] == username:
        #         flag = False
        #         data['username_msg'] = 'Username already exists'

        # find = db.users.find_one({"username": str(username)})
        # if find is not None:
        #     flag = False
        #     data['username_msg'] = 'Username already exists'

        # for ch in username:
        #     if ch not in string.ascii_letters and ch not in string.digits:
        #         flag = False
        #         data['username_msg'] = 'Username can contain [a-z][A-z][0-9] only.'

        if len(password) < 6:
            flag = False
            data['password_msg'] = 'Password length must be at least 6.'

        elif password != c_password:
            flag = False
            data['c_password_msg'] = 'Passwords did not match.'

        # find = db.users.find_one({"email": str(email)})
        # if find is not None:
        #     flag = False
        #     data['email_msg'] = 'Email already exists'

        # if '@' not in email:
        #     flag = False
        #     data['email_msg'] = 'Email format is not correct'
        # elif '.' not in email.split('@')[1]:
        #     flag = False
        #     data['email_msg'] = 'Email format is not correct'
        # else:
        #     for user in users:
        #         if user["email"] == email:
        #             flag = False
        #             data['email_msg'] = 'Email already exists'

        if len(phone_number) < 11:
            flag = False
            data['phone_number_msg'] = 'Phone Number must contain 11 digits'

        for ch in phone_number:
            if ch not in string.digits:
                flag = False
                data['phone_number_msg'] = 'Phone Number can contain only digits'

        if flag is True:
            user_data = {}

            user_data["name"] = data["name"]
            user_data["username"] = session["username"]
            user_data["email"] = session["email"]
            user_data["phone_number"] = data["phone_number"]

            user_data["institution"] = data["institution"]
            user_data["address"] = data["address"]
            user_data["dob"] = data["dob"]
            user_data["imgurl"] = data["imgurl"]
            user_data["bio"] = data["bio"]

            user_data["cf_handle"] = data["cf_handle"]
            user_data["topcoder_handle"] = data["topcoder_handle"]
            user_data["hackerrank_handle"] = data["hackerrank_handle"]
            user_data["codechef_handle"] = data["codechef_handle"]
            user_data["uhunt_handle"] = data["uhunt_handle"]

            user_data["github"] = data["github"]
            user_data["linkedin"] = data["linkedin"]

            user_data["password"] = sha256_crypt.encrypt(data["password"])


            db.child("Users").child(str(session['uid'])).set(user_data)
            return showProfile()

        return render_template('/profile/editProfile.html',user_data=data)



@app.route('/show_edit_profile/')
def show_edit_profile():
    if 'username' not in session.keys():
        return signin(None, "/show_edit_profile/")

    data = db.child("Users").child(str(session['uid'])).get().val()
    # print(data)
    user_data ={}
    for x in data:
        user_data[x] = data[x]
    print(user_data)


    if 'firstTime' is user_data.keys():
        user_data['firstTime']= True
    else:
        user_data['firstTime'] = False
    return render_template("/profile/editProfile.html",user_data=user_data)


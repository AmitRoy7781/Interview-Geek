import string
from flask import render_template, request, redirect, session, Blueprint
from iGeekFirebase.firebase import firebase
from passlib.hash import sha256_crypt

db = firebase.database()
auth = firebase.auth()

app = Blueprint('auth', __name__)


def getHash(input):
    hash_value = 0
    p = 1
    base = 67
    mod = 961748927
    for x in input:
        hash_value += (ord(x) * p)
        hash_value %= mod
        p = p * base
        p %= mod

    return str(hash_value)

def verify_hash(password1,password2):
    return getHash(password1)==password2



@app.route("/auth/signup")
def signUp(data=None):

    if 'username' in session.keys():
        return redirect('/')
    return render_template('auth/signup.html', userinfo=data)



@app.route("/auth/signup-validation", methods=['POST', 'GET'])
def signup_validation():
    if request.method == 'POST':
        data = request.form.to_dict()
        # print(data)
        name = data['name']
        username = data['username']
        password = data['password']
        c_password = data['c_password']
        email = data['email']
        phone_number = data['phone_number']
        flag = True

        if len(name)<6:
            flag = False
            data['name_msg'] = 'Name must be atleast 6 characters.'

        for ch in name:
            if ch not in string.ascii_letters and ch != ' ':
                flag = False
                data['name_msg'] = 'Name can contain [a-z][A-Z] and whitespace only.'

        if len(username) < 6:
            flag = False
            data['username_msg'] = 'Username must be atleast 6 characters.'

        user_data = db.child("Users").get().val()
        users = []

        for user in user_data:
            users.append(user_data[user])

        for user in users:
            if user["username"]==username:
                flag = False
                data['username_msg'] = 'Username already exists'

        # find = db.users.find_one({"username": str(username)})
        # if find is not None:
        #     flag = False
        #     data['username_msg'] = 'Username already exists'

        for ch in username:
            if ch not in string.ascii_letters and ch not in string.digits:
                flag = False
                data['username_msg'] = 'Username can contain [a-z][A-z][0-9] only.'

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

        if '@' not in email:
            flag = False
            data['email_msg'] = 'Email format is not correct'
        elif '.' not in email.split('@')[1]:
            flag = False
            data['email_msg'] = 'Email format is not correct'
        else:
            for user in users:
                if user["email"] == email:
                    flag = False
                    data['email_msg'] = 'Email already exists'

        if len(phone_number) < 11:
            flag = False
            data['phone_number_msg'] = 'Phone Number must contain 11 digits'

        for ch in phone_number:
            if ch not in string.digits:
                flag = False
                data['phone_number_msg'] = 'Phone Number can contain only digits'

        if flag is True:
            data.pop('c_password')
            data["password"] = getHash(password)

            data["address"] = "N/A"
            data["dob"] = "N/A"
            data["institution"] = "N/A"
            data["imgurl"] = "https://firebasestorage.googleapis.com/v0/b/interview-geek.appspot.com/o/anonymous.png?alt=media&token=25f83f1c-ec01-49bc-a8f3-dad6e4a786eb"
            data["bio"] = "N/A"

            data["cf_handle"] = "N/A"
            data["topcoder_handle"] = "N/A"
            data["hackerrank_handle"] = "N/A"
            data["codechef_handle"] = "N/A"
            data["uhunt_handle"] = "N/A"

            data["github"] = "N/A"
            data["linkedin"] = "N/A"


            # print(data)
            auth.create_user_with_email_and_password(email,password)
            auth.sign_in_with_email_and_password(email,password)

            # data["uid"] = auth.current_user["localId"]
            db.child("Users").child(str(auth.current_user["localId"])).set(data)

            return redirect('/auth/signin')

        # print(data)
        return signUp(data)


@app.route("/auth/signin")
def signin(data=None,target=None):
    if target==None:
        target = "/"
    return render_template('auth/signin.html',userinfo=data,target=target)


@app.route("/auth/signin-validation", methods=['POST', 'GET'])
def login_validation():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        username = data['username']
        # email = data['email']
        password = data['password']
        target = data['target']



        user_data = db.child("Users").get().val()
        users = []

        for user in user_data:
            users.append(user_data[user])

        flag = False

        for user in users:
            if user["username"] == username:
                flag = True
                break

        if flag == False:
            data['username_msg'] = 'Username does not Exist'

        email = ""
        for user in users:
            if user["username"] == username and verify_hash( password,user["password"]) != True:
                flag = False
                data['password_msg'] = 'Wrong password. Try again.'
                break
            elif user["username"] == username and verify_hash( password,user["password"]) == True:
                flag = True
                email = user["email"]

        if flag == False:
            return signin(data,target)


        auth.sign_in_with_email_and_password(email,password)
        print(str(auth.current_user["localId"]))
        print(db.child("Users").child(str(auth.current_user["localId"])).get().val())
        imgurl = db.child("Users").child(str(auth.current_user["localId"])).get().val()["imgurl"]
        session['username'] = username
        session['email'] = email
        session['uid'] = auth.current_user['localId']
        session['imgurl'] = imgurl
        print(imgurl)
        # print(auth.current_user)
        return redirect(target)


@app.route("/auth/logout")
def logout():
    if 'username' in session.keys():
        session.pop('username')
    if 'email' in session.keys():
        session.pop('email')
    if 'uid' in session.keys():
        session.pop('uid')

    if 'imgurl' in session.keys():
        session.pop('imgurl')

    return redirect('/')
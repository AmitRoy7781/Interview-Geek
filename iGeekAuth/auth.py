import string
from flask import render_template, request, redirect, session, Blueprint
from iGeekFirebase.firebase import auth

app = Blueprint('auth', __name__)


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

        if len(phone_number) < 11:
            flag = False
            data['phone_number_msg'] = 'Phone Number must contain 11 digits'

        for ch in phone_number:
            if ch not in string.digits:
                flag = False
                data['phone_number_msg'] = 'Phone Number can contain only digits'

        if flag is True:
            data.pop('c_password')
            auth.create_user_with_email_and_password(email,password)
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
        email = data['email']
        password = data['password']

        if username=="":
            data['username_msg'] = 'Username does not Exist'
            data['password_msg'] = ""
            return signin(data)

        try:
            session['username'] = username
            auth.sign_in_with_email_and_password(email,password)
            return redirect("/")
        except:
            data['username_msg'] = 'Wrong Username'
            data['password_msg'] = 'Password did not matched with email. Try again.'
            return signin(data)



@app.route("/auth/logout")
def logout():
    if 'username' in session.keys():
        session.pop('username')

    return redirect('/')
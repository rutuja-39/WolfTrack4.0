import os
from flask import Blueprint, session, request, redirect, render_template, current_app, make_response, url_for,send_from_directory
from flask_login import LoginManager, login_user, UserMixin
from datetime import datetime, timedelta


admin_login_route = Blueprint('admin_login', __name__)
login_manager = LoginManager()
headers = {'Content-Type': 'text/html'}

data = {
    "wishlist": ["Microsoft", "Google", "Uber"],
    "inprogress": ["Twitter", "Pearson"],
    "applied": ["Amazon", "NetApp"],
    "offers": ["Perfios"]
}

upcoming_events = [
    {"duedate": "28th Sept, 2021",
     "company": "Apple"
     },
    {"duedate": "19th Dec, 2021",
     "company": "Microsoft"
     },   
    {"duedate": "21st Dec, 2021",
     "company": "Amazon"
     },
    {"duedate": "21st Dec, 2021",
     "company": "Amazon"
     },
    {"duedate": "21st Dec, 2021",
     "company": "Amazon"
     }
]


@admin_login_route.record_once
def on_load(state):
    login_manager.init_app(state.app)

@login_manager.user_loader
def load_user(userid):
    return User(session['userinfo']['userid'])

@admin_login_route.before_app_request
def before_request():
    session.modified = True
    current_app.permanent_session_lifetime = timedelta(minutes=30)
    if request.endpoint != 'login_manager.login':
        if 'userinfo' not in session:
            pass

class User(UserMixin):
    def __init__(self, username) -> None:
        self.username = username

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True


def is_valid(username, password):
    ''' Validate the username and password with DB '''
    return True


@admin_login_route.route('', methods=["GET", "POST"])
def login():
    print("Admin Route")
    if request.method == 'GET':
        return make_response(render_template('admin_landing.html'), 200, headers)
    username = request.form['username']
    password = request.form['password']
    if not is_valid(username, password):
        pass
    user = User(username)
    session['userinfo'] = {'userid': username}
    user.id = username
    if request.method == 'POST':
        login_user(user)

    return make_response(render_template('admin_landing.html'), 200, headers)
    #return redirect(url_for('main_login_route.admin_landing'))

@admin_login_route.route("/render_resume")
def tos():
    workingdir = os.path.abspath(os.getcwd())
    print("dir")
    print(workingdir)
    filepath = workingdir + '/static/files/'
    return send_from_directory(filepath, 'resume.pdf')
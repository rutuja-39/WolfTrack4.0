'''
MIT License

Copyright (c) 2024 MD NAZMUL HAQUE, KISHAN KUMAR GANGULY, RAVI 

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import os
from flask import Flask, request, render_template, make_response, redirect,url_for,send_from_directory, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField 
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired, EqualTo
from werkzeug.utils import redirect
from Controller.send_email import *
from Controller.send_profile import *
from Controller.ResumeParser import *
from Utils.jobprofileutils import *
import os
from flask import send_file, current_app as app
from Controller.chat_gpt_pipeline import pdf_to_text,chatgpt
from Controller.data import data, upcoming_events, profile
from Controller.send_email import *
from dbutils import add_job, create_tables, add_client, delete_job_application_by_job_id ,find_user, get_job_applications, get_job_applications_by_status, update_job_application_by_id, get_user_by_username_role
from login_utils import login_user
import requests
import urllib.parse


app = Flask(__name__)
# api = Api(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"  # SQLite URI
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)
database = "database.db"
"""
CREATE TABLE client (
    id INTEGER NOT NULL,
    name VARCHAR(20) NOT NULL,
    username VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(80) NOT NULL,
    usertype VARCHAR(20) NOT NULL,
    PRIMARY KEY (id)
);
"""
create_tables(database)

# class Client(db.Model,UserMixin):
#     __tablename__ = 'client'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), nullable=False)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     password = db.Column(db.String(80), nullable=False)
#     usertype = db.Column(db.String(20), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    name = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Name"})
    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    usertype = SelectField(render_kw={"placeholder": "Usertype"}, choices=[('admin', 'Admin'), ('student', 'Student')])
    submit = SubmitField('Register')

@app.route('/')
def index():
    return render_template('index.html')

@app.before_request
def require_login():
    # Define routes that do not require login
    open_routes = ['/login', '/signup', '/static']
    # Bypass static files to prevent them from being blocked
    if request.path.startswith('/static/'):
        return  # Allow static files
    # Get the current path
    path = request.path

    # Debug statement to check current path
    print(f"Request path: {path}")

    # Allow open routes and API static files
    if any(path.startswith(route) for route in open_routes):
        print(f"Path '{path}' is open, no login required.")
        return  # Allow open routes

    # Redirect to login page if 'user_id' is not in the session
    if 'user_id' not in session:
        print(f"User not logged in, redirecting to login.")
        flash('You need to be logged in to access this page.', 'danger')
        return redirect(url_for('login'))


def isLoggedIn():
    return session['user_id']!=None and session['type']!=None

@app.route('/logout',methods=['GET', 'POST'])
def logout():
    session['type'] = ''
    session['user_id'] = None
    session.clear()
    return redirect(url_for('login'))


@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_role = request.form['user_role']

        user = get_user_by_username_role(username, user_role, database)
        if user and bcrypt.check_password_hash(user[3], password):
            # User authenticated successfully
            login_user(app,user)

            if user_role == 'admin':
                return redirect(url_for('admin', data=username))  # Replace with actual route name
            elif user_role == 'student':
                return redirect(url_for('student', data=username))  # Replace with actual route name
        else:
            flash('Invalid username, password, or role. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        user = find_user(str(form.username.data),database)
        if user:
            flash('Username already exists. Please choose a different username.', 'danger')
            return render_template('signup.html',form = RegisterForm())
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_client = [form.name.data,form.username.data, hashed_password, form.usertype.data]
        add_client(new_client,database)
        return redirect(url_for('login'))

    return render_template('signup.html',form = RegisterForm())

@app.route('/admin',methods=['GET', 'POST'])
def admin():
    data_received = request.args.get('data')
    user = find_user(str(data_received),database)
    ##Add query
    return render_template('admin_landing.html', user=user)


@app.route('/student',methods=['GET', 'POST'])
def student():
    if(isLoggedIn()==False):
        return redirect(url_for('login'))
    user_name = session['user_name']
    user = find_user(user_name,database)

    jobapplications = get_job_applications(user_name, database)
    return render_template('home.html', user=user, jobapplications=jobapplications)
    # return render_template('home-2.html', user=user, jobapplications=jobapplications)

@app.route('/student/<status>', methods=['GET', 'POST'])
def get_job_application_status(status):
    data_received = request.args.get('data')
    print("faul ", data_received)
    user = find_user(str(data_received), database)

    if status:
        job_applications = get_job_applications_by_status(database, status)
    else:
        job_applications = get_job_applications(database)

    return render_template('home.html', user=user, jobapplications=job_applications)


@app.route("/admin/send_email", methods=['GET','POST'])
def send_email():
    comments = request.form['comment']
    email = 'elliotanderson506@gmail.com'
    s_comment_email(email,comments)
    return make_response(render_template('admin_landing.html'), 200,{'Content-Type': 'text/html'})

@app.route("/admin/render_resume")
def tos():
    workingdir = os.path.abspath(os.getcwd())
    filepath = workingdir + '/static/files/'
    return send_from_directory(filepath, 'resume2.pdf')

@app.route("/add_job_application", methods=['POST'])
def add_job_application():
    if request.method == 'POST':
        company = request.form['company']
        location = request.form['location']
        jobposition = request.form['jobposition']
        salary = request.form['salary']
        status = request.form['status']
        user_id = request.form['user_id']

        job_data = [company, location, jobposition, salary, status]
        # Perform actions with the form data, for instance, saving to the database
        add_job(job_data,database)

        flash('Job Application Added!')
        # Redirect to a success page or any relevant route after successful job addition
        return redirect(url_for('student', data=user_id))

@app.route('/student/update_job_application',methods=['GET','POST'])
def update_job_application():
    if request.method == 'POST':
        job_id = request.form['job_id']
        company = request.form['company']
        location = request.form['location']
        jobposition = request.form['jobposition']
        salary = request.form['salary']
        status = request.form['status']
        user_name = session['user_name']

        # Perform the update operation
        update_job_application_by_id( job_id, company, location, jobposition, salary, status, database)  # Replace this with your method to update the job

        flash('Job Application Updated!')
        # Redirect to a success page or any relevant route after successful job update
        return redirect(url_for('student', data=user_name))

@app.route('/student/delete_job_application', methods=['POST'])
def delete_job_application():
    if request.method == 'POST':
        job_id = request.args.get('job_id')
        user_name = request.args.get('user_name')
        delete_job_application_by_job_id(job_id,database)  
        flash('Job Application Deleted!')
        return redirect(url_for('student', data=user_name)) 

@app.route('/student/add_New',methods=['GET','POST'])
def add_New():
    company_name = request.form['fullname']
    location = request.form['location_text']
    Job_Profile = request.form['text']
    salary = request.form['sal']
    user = request.form['user']
    password = request.form['pass']
    email = request.form['user_email']
    sec_question = request.form['starting_date']
    sec_answer = request.form['starting_date']
    notes = request.form['notes']
    date_applied = request.form['starting_date']

    s_email(company_name,location, Job_Profile,salary, user,password,email,sec_question,sec_answer,notes,date_applied)
    return render_template('home.html', data=data, upcoming_events=upcoming_events, user=user)

@app.route('/student/send_Profile',methods=['GET','POST'])
def send_Profile():
    emailID = request.form['emailID']
    s_profile(data,upcoming_events, profile,emailID)

    print("Email Notification Sent")
    '''data_received = request.args.get('data')
    print('data_receivedddd->>>> ', data_received)
    user = find_user(str(data_received))
    print('Userrrrrr', user)'''
    user_id = request.form['user_id']
    user = request.form['user_id']
    print('==================================================================', user)
    
    user = find_user(str(user),database)

    data_received = request.args.get('data')
    user = find_user(str(data_received),database)

    return render_template('home.html', data=data, upcoming_events=upcoming_events, user=user)


@app.route('/student/job_profile_analyze', methods=['GET', 'POST'])
def job_profile_analyze():
    if request.method == 'POST':
        job_profile = request.form['job_profile']
        skills = extract_skills(job_profile)
        skills_text = ', '.join(skills)
        return render_template('job_profile_analyze.html', skills_text=skills_text, job_profile=job_profile)
    return render_template('job_profile_analyze.html', skills_text='', job_profile='')

filename=""
@app.route("/student/upload", methods=['POST'])
def upload():
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(APP_ROOT, 'Controller\\resume\\')

    if not os.path.isdir(target):
        os.mkdir(target)
    if len(os.listdir(target)) != 0:
        os.remove(target + os.listdir(target)[0])

    for file in request.files.getlist("file"):
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)

    user = request.form['user_id']
    
    user = find_user(str(user),database)
    print('Userrrrrr', user)


    return render_template("home.html", data=data, upcoming_events=upcoming_events, user=user)

@app.route('/student/analyze_resume', methods=['GET'])
def view_ResumeAna():
    return render_template('resume_analyzer.html')

@app.route('/student/companiesList', methods=['GET'])
def view_companies_list():
    return render_template('companies_list.html')


@app.route('/student/analyze_resume', methods=['POST'])
def analyze_resume():
    jobtext = request.form['jobtext']
    os.chdir(os.getcwd()+"/Controller/resume/")
    output = resume_analyzer(jobtext, str(os.listdir(os.getcwd())[0]))
    os.chdir("..")
    os.chdir("..")
    return render_template('resume_analyzer.html', data = output)

@app.route("/student/display/", methods=['POST','GET'])
def display():
    path = os.getcwd()+"/Controller/resume/"
    filename = os.listdir(path)
    if filename:
        return send_file(path+str(filename[0]),as_attachment=True)
    else:
        user = request.form['user_id']
        user = find_user(str(user),database)
        return render_template('home.html', user=user, data=data, upcoming_events=upcoming_events)

@app.route('/student/chat_gpt_analyzer/', methods=['GET'])
def chat_gpt_analyzer():
    files = os.listdir(os.getcwd()+'/Controller/resume')
    pdf_path = os.getcwd()+'//Controller/resume/'+files[0]
    text_path = os.getcwd()+'//Controller/resume_txt/'+files[0][:-3]+'txt'
    with open(text_path, 'w'):
        pass
    pdf_to_text(pdf_path, text_path)
    suggestions = chatgpt(text_path)
    flag = 0
    final_sugges_send = []
    final_sugges = ""

    # Initialize an empty string to store the result
    result_string = ""

    # Iterate through each character in the original string
    for char in suggestions:
        # If the character is not a newline character, add it to the result string
        if char != '\n':
            final_sugges += char
    sections = final_sugges.split("Section")
    for section in sections:
        section = section.strip()  # Remove leading and trailing whitespace
        # if section:  # Check if the section is not empty (e.g., due to leading/trailing "Section")
        #     print("Section:", section)
    sections = sections[1:]
    section_names = ['Education', 'Experience','Skills', 'Projects']
    sections[0] = sections[0][3:]
    sections[1] = sections[1][3:]
    sections[2] = sections[2][3:]
    sections[3] = sections[3][3:]
    return render_template('chat_gpt_analyzer.html', suggestions=sections, pdf_path=pdf_path, section_names = section_names)

@app.route('/student/job_search')
def job_search():
    return render_template('job_search.html')

@app.route('/student/job_search/result', methods=['POST'])
def search():
    job_title = urllib.parse.quote(request.form['job_title'])
    location = urllib.parse.quote(request.form['location'])
    minSalary = request.form['minSalary']
    maxSalary = request.form['maxSalary']
    job_type = request.form['job_type']
    company = urllib.parse.quote(request.form['company'])
    query = "what_phrase="+job_title
    if(len(minSalary)>0): query+="&salary_min="+minSalary
    if(len(maxSalary)>0): query+="&salary_max="+maxSalary
    if(job_type=="full_time"): query+="&full_time=1"
    if(job_type=="part_time"): query+="&part_time=1"
    if(len(company)>0): query+="&company="+company

    adzuna_url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id=575e7a4b&app_key=35423835cbd9428eb799622c6081ffed&"+query
    try:
        response = requests.get(adzuna_url)
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('results', [])
            return render_template('job_search.html', jobs=jobs)
        else:
            return "Error fetching job listings"
    except requests.RequestException as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)

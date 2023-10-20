from flask import Blueprint
from flask import Flask, render_template, url_for, request
from flask_login import login_required, logout_user, current_user
from werkzeug.utils import redirect,send_from_directory
from Controller.send_email import *
from Controller.send_profile import *
from Controller.ResumeParser import *
import os
from flask import send_file, current_app as app
from Controller.data import data, upcoming_events, profile
from Controller.chat_gpt_pipeline import pdf_to_text,chatgpt

home_route = Blueprint('home_route', __name__)


@home_route.route('', methods=['GET'])
def home():
    if current_user.is_authenticated:
        return render_template('home.html', data=data, upcoming_events=upcoming_events)
    else:
        return render_template('main_login.html')


@home_route.route('/view', methods=['GET'])
@login_required
def view():
    card_selected = request.args.get('user')
    return render_template('view_list.html', data=data, upcoming_events=upcoming_events)

@home_route.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect("/")

@home_route.route('/add_New',methods=['GET','POST'])
#@login_required
def add_New():
    #print(request.method)

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

    print("Adding New...")
    s_email(company_name,location, Job_Profile,salary, user,password,email,sec_question,sec_answer,notes,date_applied)
    print("Added Company to List")
    print("Email Notification Sent")
    return render_template('home.html', data=data, upcoming_events=upcoming_events)

@home_route.route('/send_Profile',methods=['GET','POST'])
def send_Profile():
    emailID = request.form['emailID']
    print("Mailing Profile...")
    s_profile(data,upcoming_events, profile,emailID)
    print("Email Notification Sent")
    return render_template('home.html', data=data, upcoming_events=upcoming_events)


filename=""
@home_route.route("/upload", methods=['POST'])
def upload():
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(APP_ROOT, 'resume/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)
    if len(os.listdir(target)) != 0:
        os.remove(target + os.listdir(target)[0])

    for file in request.files.getlist("file"):
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)

    return render_template("home.html", data=data, upcoming_events=upcoming_events)

@home_route.route('/resumeAnalyzer', methods=['GET'])
@login_required
def view_ResumeAna():
    return render_template('resume_analyzer.html')

@home_route.route('/companiesList', methods=['GET'])
@login_required
def view_companies_list():
    return render_template('companies_list.html')


@home_route.route('/findJobs', methods=['GET'])
@login_required
def view_jobs(): 
    import json
    f = open('Controller/scrap.json')
    data = json.load(f)
    return render_template('find_jobs.html', data = (data))

@home_route.route('/analyze_resume', methods=['POST'])
@login_required
def analyze_resume():
    jobtext = request.form['jobtext']
    print(jobtext)
    os.chdir(os.getcwd()+"/Controller/resume/")
    output = resume_analyzer(jobtext, str(os.listdir(os.getcwd())[0]))
    os.chdir("..")
    os.chdir("..")
    print(output)
    return render_template('resume_analyzer.html', data = output)

@home_route.route("/display/", methods=['POST','GET'])
def display():
    path = os.getcwd()+"/Controller/resume/"
    filename = os.listdir(path)
    print(filename, path)
    return send_file(path+str(filename[0]), attachment_filename= str(filename[0]))


@home_route.route('/chat_gpt_analyzer/', methods=['GET'])
def chat_gpt_analyzer():
    files = os.listdir(os.getcwd()+'/Controller/resume')
    print(files[0])
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
    print(sections)
    sections = sections[1:]
    section_names = ['Education', 'Experience','Skills', 'Projects']
    sections[0] = sections[0][3:]
    sections[1] = sections[1][3:]
    sections[2] = sections[2][3:]
    sections[3] = sections[3][3:]
    return render_template('chat_gpt_analyzer.html', suggestions=sections, pdf_path=pdf_path, section_names = section_names)

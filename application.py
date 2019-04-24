from flask import Flask, render_template, flash, request, send_file
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import CommandAndControl
from request import Request
from user import user
import uuid
from datetime import datetime
from pathlib import Path
import subprocess
# App config.
DEBUG = True
application = Flask(__name__)
application.config.from_object(__name__)
application.config['SECRET_KEY'] = '7d451f27d441f27567d441f2b6176a'
requests = []


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:')#, validators=[validators.required(), validators.Length(min=6, max=35)])
    # password = TextField('Password:', validators=[True])
 
@application.route("/", methods=['GET', 'POST'])
def submit_gen_request():
    form = ReusableForm(request.form)
 
    print (form.errors)
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        print (name, " ", email)
 
    if form.validate():
        r = Request(name, email, user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now())
        requests.append(r)
        # CommandAndControl.download_all_requests(requests)
        flash('Thanks for the submission, your receipt is ' + r.uuid)

    # else:
        # flash('Error: All the form fields are required. ')
 
    return render_template('hello.html', form=form)


@application.route("/get-my-request", methods=['GET', 'POST'])
def getmyrequest():
    form = ReusableForm(request.form)
 
    print (form.errors)
    if request.method == 'POST':
        name=request.form['name']
        print (name, " ")
 
    if form.validate():
        space_seperated_ids = ""
        for input_uuid in name.split(','):
            print("input uuid: ", input_uuid)
            space_seperated_ids += input_uuid + " "
            
        space_seperated_ids = space_seperated_ids[:-1]
        print(space_seperated_ids)
        return_id = str(uuid.uuid4())
        # subprocess.call(r'pwd')
        subprocess.call(r'cd output; zip -r ' + return_id + '.zip ' + space_seperated_ids, shell=True)
        return send_file('output/' + return_id + '.zip', as_attachment=True)
        
            # for r in requests:
            #     print("r.uuid:", r.uuid)
            #     if r.uuid == input_uuid:
            #         print("Should be sending a file")
            #         if Path('output/' + input_uuid + '.zip').is_file():
            #             print("sending file")
            #             return send_file('output/' + input_uuid + '.zip', as_attachment=True)
            #         else:
            #             print("File does not exist")
            #             flash('File has not been downloaded yet: ' + input_uuid)
            #         # send_my_file(input_uuid)
    # else:
        # flash('Error: All the form fields are required. ')
        
    return render_template('get-my-request.html', form=form) 

@application.route("/google-research", methods=['GET', 'POST'])
def googleresearch():
    form = ReusableForm(request.form)
 
    print (form.errors)
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        print (name, " ", email)
 
    if form.validate():
# Save the comment here.
        r = Request(name, email, user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now())
        requests.append(r)
        # CommandAndControl.download_all_requests(requests)
        flash('Thanks for registration, your receipt is ' + r.uuid)


        
    else:
        flash('Error: All the form fields are required. ')
        
    return render_template('research.html', form=form) 

@application.route("/download", methods=['GET', 'POST'])
def download_requests():
    CommandAndControl.download_all_requests(requests)
    # requests = []
    return render_template('download.html') 

if __name__ == "__main__":
    application.debug = True
    application.run()

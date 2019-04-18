from flask import Flask, render_template, flash, request, send_file
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import CommandAndControl
from request import Request
from user import user
from datetime import datetime

# App config.
DEBUG = True
application = Flask(__name__)
application.config.from_object(__name__)
application.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
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
# Save the comment here.
        print("we in bois")
        for r in requests:
            if r.uuid == name:
                print("should be getting it")
                return send_file('output/' + r.uuid + '.zip', as_attachment=True)
    else:
        flash('Error: All the form fields are required. ')
        
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
    application.run(host='0.0.0.0')

#!/var/www/html/FlaskApp/cs2080fileshare/.venv/bin python
import sys
print("prefix = " + sys.prefix)
print("base_prefix = " + sys.base_prefix)

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm, CSRFProtect
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length
from flask import send_file, session, request
from werkzeug.utils import secure_filename
from os import walk, path, makedirs

import cs2080fileshare.loginHandling as loginHandler

app = Flask(__name__)

bootstrap = Bootstrap(app)
csrf = CSRFProtect(app)

#SSL Certificate code

#@app.route("/")
#def hello():
#    return "Hello World!"

if __name__ == "__main__":
    app.run(debug = True, ssl_context=('/etc/apache2/ssl/apache-selfsigned.crt', '/etc/apache2/ssl/apache-selfsigned.key'))

class LoginForm(FlaskForm):
    username = StringField("username:", validators=[DataRequired(), Length(5, 40)])
    password = PasswordField("password:", validators=[DataRequired(), Length(5,40)])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    username = StringField("username:", validators=[DataRequired(), Length(5,40)])
    password = PasswordField("password:", validators=[DataRequired(), Length(5,40)])
    confirmpassword = PasswordField("confirm password:", validators=[DataRequired(), Length(5,40)])
    submit = SubmitField('Submit')

class UploadForm(FlaskForm):
    upload_file = FileField()
    submitupl = SubmitField('Upload')

class PermissionForm(FlaskForm):
    allowedUsers = StringField("users allowed to download:")
    submit = SubmitField("Submit")


#TODO: Replace with mySQL implementation
def getUserFileList(username):
    filepath = "/var/www/html/FlaskApp/cs2080fileshare/data/" + username
    filenames = next(walk(filepath), (None, None, []))[2]
    return filenames

def getUserContent(username):
        filelist = getUserFileList(username)
        fileHtmlList = ""
        for filename in filelist:
            fileHtmlList = fileHtmlList + '<br><a href="/download?user='+ username + '&file=' + filename + '">Download ' + filename + '</a>'
        return fileHtmlList

#TODO: Replace with mySQL implementation
def getFilePath(username, filename):
    return "/var/www/html/FlaskApp/cs2080fileshare/data/" + username + "/" + filename



@app.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    uplForm = UploadForm()
    html = "index.html" #either index.html or user.html depending on whether user is logged in
    message = ""
    userSpecificContent = ""
    
    # check login
    if form.submit.data and form.validate_on_submit():
        username = form.username.data
        form.username.data = ""
        password = form.password.data
        form.password.data = ""
        loginSuccess = loginHandler.checkPassword(username, password)

        # successful login; add user to session
        if loginSuccess:
            userSpecificContent = getUserContent(username)
            message = "Login successful; logged in as " + username
            html = "user.html"
            session["username"] = username
            return redirect("/files", code=302)
        #unsuccessful login; give error
        else:
            message = "Login unsuccessful"

    #display page
    return render_template("index.html", form=form, message=message)


#this is the user page; where the user uploads/downloads files and changes permissions
@app.route("/files", methods=["GET", "POST"])
def files():
    form = UploadForm()
    permissionForm = PermissionForm()

    if "username" in session and session["username"]:
        # file upload
        if form.submitupl.data and form.validate_on_submit():
            if form.upload_file.data:
                filename = secure_filename(form.upload_file.data.filename)
                filepath = "/var/www/html/FlaskApp/cs2080fileshare/data/" + session["username"]
                if not path.exists(filepath):
                    makedirs(filepath)
                form.upload_file.data.save(filepath + "/" + filename)

        return render_template("user.html", username=session["username"], uploadform = form, permform=permissionForm, usercontent = getUserContent(session["username"]))
    else:
        return "<p>ERROR: Not logged in</p>"


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    message = ""
    
    if form.validate_on_submit():
        username = form.username.data
        form.username.data = ""
        password = form.password.data
        form.password.data = ""
        confpassword = form.confirmpassword.data
        form.confirmpassword.data = ""
        
        if password == confpassword:
            loginHandler.addAccount(username, password)
            message = "registration successful"
            session["username"] = username
            return redirect("/files", code=302)
        else:
            message = "password and confirm password don't match"
    
    return render_template("register.html", form=form, message=message)


@app.route("/download", methods=["GET", "POST"])
def download():
    username = request.args.get("user", None)
    if username == session["username"]:
        filename = request.args.get("file", None)
        if filename:
            filepath = getFilePath(username, filename)
            return send_file(filepath, as_attachment=True)
        else:
            return "<p>ERROR: Invalid filename</p>"
    else:
        return "<p>ERROR: No access</p>"


@app.route("/test", methods=["GET", "POST"])
def test():
    return render_template("wordpressthing.html")

def hello():
    return "<p>hello world</p>"
if __name__ == "__main__":
    app.run(ssl_context='adhoc')

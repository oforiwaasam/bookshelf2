import os
from dotenv import load_dotenv
load_dotenv() # running this will create environment variables
from flask import Flask, render_template, request, url_for, flash, redirect
# For the database
from flask_sqlalchemy import SQLAlchemy
from forms import SignupForm, LoginForm

app = Flask(__name__)
# Define a new database below and tell it to use the app above
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'akdhej klklejio jh'
# Where our database will be located (in site.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
  
  #### Return a rendered index.html file
  return render_template("index.html")

# route accepts both get and post requests
@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  form.username(placeholder="username")
  #### Return a rendered login.html file
  return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
  if form.validate_on_submit(): # checks if entries are valid
  #### Return a rendered signup.html file
  return render_template("signup.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, url_for, flash, redirect
# from flask_sqlalchemy import SQLAlchemy
from forms import SignupForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'akdhej klklejio jh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db = SQLAlchemy(app)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
  
  #### Return a rendered index.html file
  return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  form.username(placeholder="username")
  #### Return a rendered login.html file
  return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
  #### Return a rendered signup.html file
  return render_template("signup.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)

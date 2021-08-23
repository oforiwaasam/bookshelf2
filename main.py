import os
from dotenv import load_dotenv
from sqlalchemy.sql.functions import user
load_dotenv() # running this will create environment variables
from flask import Flask, render_template, request, url_for, flash, redirect, session
# from flask import logout_user
from flask_login import UserMixin, LoginManager, current_user, login_required, login_user, logout_user
from flask_behind_proxy import FlaskBehindProxy 
# For the database
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from forms import SignupForm, LoginForm
from encryption import *


app = Flask(__name__)
# Define a new database below and tell it to use the app above
db = SQLAlchemy(app)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = 'akdhej klklejio jh'
# Where our database will be located (in site.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#Create login manager object, telling it which app we're using         
login_manager = LoginManager(app)


# Database model used to store user's notes information
class Note(db.Model):
    # define database columns and their types
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    # setting timezone as well as date (func will automatically add current date and time to note)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # setting relationship between note and user object using a foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# Database model used to store User information
class User(db.Model, UserMixin):
    # define database columns and their types
    # unique means users cannot share the same values in that column
    # find out what nullable means
    # __tablename__ = 'flasklogin-users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # password can store 200 characters because of hashing
    password = db.Column(db.String(200), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='avatar.png')
    account_date = db.Column(db.DateTime(timezone=True), index=False, unique=False, nullable=True)
    last_login = db.Column(db.DateTime(timezone=True), index=False, unique=False, nullable=True)
    # notes all of the notes that a user has created
    notes = db.relationship('Note') # Note here is the name of Note object created below

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


# anyone who visits this page will see page
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
  
  #### Return a rendered index.html file
  return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
  """
    route accepts GET requests when users land on the page and POST 
    requests when users attempt to submit a form
  """
    # Bypass if user is logged in (check this out)
  if current_user.is_authenticated:
    return redirect(url_for('profile'))

  form = LoginForm()
  if form.validate_on_submit(): # checks if entries are valid
        logged_user = User.query.filter_by(username=form.username.data).first()

        if logged_user and logged_user.check_password(password=form.password.data):
          login_user(logged_user)
          flash("You've been successfully logged in", 'success')
          next_page = request.args.get('next')
          return redirect(next_page or url_for('profile'))

        # Username does not exist
        flash('Invalid username or password', 'danger')
        return redirect(url_for('login'))

  #### Return a rendered login.html file
  return render_template('login.html', form=form, user=current_user)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  """
    validate on submit will only trigger if the incoming request is 
    a POST request containing form information, hence we don't check
    that request.method is equal to POST
  """
  form = SignupForm()
  
  if form.validate_on_submit(): # checks if entries are valid
        # Check database if username is already in use
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user is not None:
            flash(f'Username {existing_user.username} is already taken', 'danger')
            return render_template('signup.html', title='Register', form=form)

        # Check database if email is already in use
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is not None:
            flash(f'Email {existing_user.email} is already taken', 'danger')
            return render_template('signup.html', title='Register', form=form)

        # User can be registered
        user = User(username=form.username.data, 
                    email=form.email.data,
                    password= encrypt_password(form.password.data)
        ) # check this out again
        
        # user.encrypt_password(form.password.data)
        db.session.add(user) # add new user to database
        db.session.commit() # Update database with new user
        login_user(user)  # Automatically logs the new user in, you can set remember to true here
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index')) # redirect user to the home page
  #### Return a rendered signup.html file
  return render_template("signup.html", form=form, user=current_user)

# user cannot access this route unless their logged in
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
  image_file = url_for('static', filename='img/' + current_user.image_file)
  #### Return a rendered index.html file
  return render_template("profile.html", user=current_user, image_file=image_file)

# user cannot access this route unless their logged in
@app.route('/logout')
@login_required
def logout():
  logout_user()
  #### Return a rendered login.html file
  return redirect(url_for('login'))


# telling Flask how we load a user
@login_manager.user_loader
def load_user(id):
    """Check if user is logged-in upon page load."""
    if id is not None:
        return User.query.get(int(id)) # get will look for the primary key
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))

if __name__ == "__main__":
    app.run(debug=True)

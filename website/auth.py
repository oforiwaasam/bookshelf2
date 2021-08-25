import os
import secrets
from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import current_user, login_required, login_user, logout_user 
from . import login_manager
from .models import User, db
from .forms import LoginForm, SignupForm, updateProfileForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
        route accepts GET requests when users land on the page and POST 
        requests when users attempt to submit a form
    """
        # Bypass if user is logged in (check this out)
    if current_user.is_authenticated:
        return redirect(url_for('auth.profile'))

    # creating an instance of login form
    form = LoginForm()
    if form.validate_on_submit(): # checks if entries are valid
        logged_user = User.query.filter_by(username=form.username.data).first()

        if logged_user and logged_user.check_password(password=form.password.data):
            login_user(logged_user)
            next_page = request.args.get('next')
            flash("You've been successfully logged in", 'success')
            return redirect(next_page or url_for('auth.profile'))

        else:
            # Username does not exist
            flash('Invalid username or password', 'danger')

    #### Return a rendered login.html file
    return render_template('login.html', form=form, user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """
        validate on submit will only trigger if the incoming request is 
        a POST request containing form information, hence we don't check
        that request.method is equal to POST
    """
    form = SignupForm()
  
    if form.validate_on_submit(): # checks if entries are valid
            # Check database if username is already in use
            # existing_user = User.query.filter_by(username=form.username.data).first()
            # if existing_user is not None:
            #     flash(f'Username {existing_user.username} is already taken', 'danger')
            #     return render_template('signup.html', title='Register', form=form)

            # # Check database if email is already in use
            # existing_user = User.query.filter_by(email=form.email.data).first()
            # if existing_user is not None:
            #     flash(f'Email {existing_user.email} is already taken', 'danger')
            #     return render_template('signup.html', title='Register', form=form)

        exist_username = User.query.filter_by(username=form.username.data).first()
        exist_email = User.query.filter_by(username=form.email.data).first()
        if exist_username is None and  exist_email is None:
            # User can be registered
            user = User(username=form.username.data, 
                        email=form.email.data
                        # password= encrypt_password(form.password.data)
            ) # check this out again
            
            user.encrypt_password(form.password.data)
            db.session.add(user) # add new user to database
            db.session.commit() # Update database with new user
            login_user(user)  # Automatically logs the new user in, you can set remember to true here
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('main.index')) # redirect user to the home page
        flash('A user already exists with that username and/or email address')
    #### Return a rendered signup.html file
    return render_template("signup.html", form=form, user=current_user)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    # Use underscore for variables you do not need
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(auth.root_path, 'static/img', picture_fn)
    form_picture.save(picture_path)

    return picture_fn


# user cannot access this route unless they are logged in
@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
  form = updateProfileForm()
  
  if form.validate_on_submit():
    if form.picture.data:
        picture_file = save_picture(form.picture.data)
        current_user.image_file = picture_file
    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('Your account has been updated!', 'success')
    return redirect(url_for('auth.profile'))

  # populating form with current user's data
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email

  image_file = url_for('static', filename='img/' + current_user.image_file)
  #### Return a rendered profile.html file
  return render_template("profile.html", form=form, user=current_user, image_file=image_file)


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
    return redirect(url_for('auth.login'))

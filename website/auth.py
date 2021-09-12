import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import current_user, login_required, login_user 
from . import login_manager
from .models import User, db
from .forms import LoginForm, SignupForm, UpdateProfileForm, SearchForm
from bestsellers import *
from book_apis import *

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
        # Query user here
        logged_user = User.query.filter_by(username=form.username.data).first()

        if logged_user and logged_user.check_password(password=form.password.data):
            login_user(logged_user, remember=form.remember.data)
            flash("You've been successfully logged in", 'success')
            next_page = request.args.get('next')
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
    # initialize Signup form
    form = SignupForm()
  
    if form.validate_on_submit(): # checks if entries are valid
        # Check database if username and email are already in use

        exist_username = User.query.filter_by(username=form.username.data).first()
        exist_email = User.query.filter_by(email=form.email.data).first()
        if exist_username is None and exist_email is None:
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
        flash('A user already exists with that username and/or email address', 'danger')
    #### Return a rendered signup.html file
    return render_template("signup.html", form=form, user=current_user)

def save_picture(form_picture):
    # generate random hex for image
    random_hex = secrets.token_hex(8)
    # Use underscore for variables you do not need
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(auth.root_path, 'static/img', picture_fn)
    # Resizing image before saving it
    output_size = (125, 125)
    new_image = Image.open(form_picture)
    new_image.thumbnail(output_size)
    new_image.save(picture_path)

    return picture_fn


# user cannot access this route unless they are logged in
@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
  # initialize profile form
  form = UpdateProfileForm()
  
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

class Book:
    def __init__(self):
        self.key = ''
        self.other_books = {}
        self.home_search = ''
        self.book_stack = {"Recent":{},"Selected":{},"Favorite":{}}
        #self.image = icons[0][1]

book = Book()

# books landing page for user when they log in
@auth.route('/books', methods=['GET', 'POST'])
@login_required
def books():
    top_books, book.other_books = homepage_bestsellers()
    book.book_stack["Recent"] = book.other_books
    image_file = url_for('static', filename='img/' + current_user.image_file)
#     book.other_books = top_books
    if request.method=='POST':
        book.key = request.form.get("q")
        book.other_books = ol_book_names(book.key)
        if(len(book.other_books.keys())==0):
            flash("Sorry No Books",'error')
        book.book_stack["Recent"] = book.other_books
        return render_template('search.html', button="Books", books=book.other_books, top_books=top_books, image_file=image_file)
    
    return render_template('books.html', top_books=top_books, image_file=image_file)


# for searching up books by name
@auth.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    image_file = url_for('static', filename='img/' + current_user.image_file)
    book.other_books = select_category("Hardcover Fiction")
    if(len(book.other_books.keys())==0):
        flash("Sorry No Books",'secondary')
    book.book_stack["Recent"] = book.other_books

    if request.method=='POST':
        book.key = request.form.get("q")
        # if log_manage.is_logged_in():
            # username = log_manage.get_username()
            # for database
            # update_search_history(username, 'Book', book.key)

        book.other_books = ol_book_names(book.key)
        if (len(book.other_books.keys()) == 0):
            flash("Sorry No Books", 'secondary')
        book.book_stack["Recent"] = book.other_books
        return render_template('search.html', button="Book", books=book.other_books, user=current_user, image_file=image_file)
        
    return render_template('search.html', button="Book", books=book.other_books, user=current_user, image_file=image_file)
        

# helper fun for book_page
def lookforbook(other_books, name):
    if(isinstance(other_books, dict)):
        for key,value in other_books.items():
            if (name in key):
                return key, value
    else:
        # for elem in other_books:
        for key,value in other_books.items():
            if (name in key ):
                return key, value
    return None, [None,None,None,None] #in case it does not work for now -> make exception later on


@auth.route("/book_page/<path:key>", methods=['GET','POST'])
def book_page(key):
    cover, book_data = lookforbook(book.other_books,key)
    image_file = url_for('static', filename='img/' + current_user.image_file)
    if cover is not None and book_data is not None:
        #prices = get_data(book_data[3])
        prices = None
        if(cover!=None and (cover not in book.book_stack["Selected"].keys())):
            print("COVERCOVERCOVER", cover)
            book.book_stack["Selected"].update({cover:book_data})
        if(request.method=='POST'):
            if(cover!=None and (cover not in book.book_stack["Favorite"].keys())):
                book.book_stack["Favorite"].update({cover:book_data})
        if prices==None:
            return render_template('book_page.html', book_title=book_data[0], author=book_data[1], web=book_data[2], cover=cover, recs = book.other_books, image_file=image_file)

        return render_template('book_page.html', book_title=book_data[0], author=book_data[1], web=book_data[2], cover=cover, recs = book.other_books, prices=prices, image_file=image_file)
    return render_template('book_page.html', book_title = "No book information found.", recs={}, image_file=image_file)


# takes you to landing page with specific bestseller category books listed (bestseller.html)
@auth.route("/search_best_seller/<string:category>", methods=['GET', 'POST'])
@login_required
def search_best_seller(category):
#     print(category)
    book.other_books = select_category(category)
    book.book_stack["Recent"] = book.other_books
    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('bestsellers.html', books=book.other_books, image_file=image_file)


@auth.route("/search_author", methods=['GET', 'POST'])
@login_required
def search_author():
    image_file = url_for('static', filename='img/' + current_user.image_file)

    if request.method=='POST':
        book.key = request.form.get("q")
        
        # if log_manage.is_logged_in():
        #     username = log_manage.get_username()
        #     update_search_history(username, 'Author', book.key)
        
        search = ol_authors(book.key)
        if(search[0]==0):
            print("IN HERE")
            book.other_books = search[1]
            if(len(book.other_books.keys())==0):
                flash("Sorry No Books",'error')
            book.book_stack["Recent"] = book.other_books
            return render_template('search.html',button="Author", books=book.other_books, image_file=image_file)
        else:
            return render_template('search.html',button="Author", subtitle=f'Did you mean.. {search[1]}', books={}, image_file=image_file)
        
    return render_template('search.html',button="Author", books={}, image_file=image_file)

@auth.route("/search_ISBN", methods=['GET', 'POST'])
@login_required
def search_ISBN():
    image_file = url_for('static', filename='img/' + current_user.image_file)

    if request.method=='POST':
        book.key = request.form.get("q")
        
        # if log_manage.is_logged_in():
        #     username = log_manage.get_username()
        #     update_search_history(username, 'ISBN', book.key)
        book.other_books = ol_isbn(book.key)
        if(len(book.other_books.keys())==0):
            flash("Sorry No Books",'error')
        book.book_stack["Recent"] = book.other_books
        return render_template('search.html',button="ISBN", books=book.other_books, image_file=image_file)
    return render_template('search.html',button="ISBN", books={}, image_file=image_file)

@auth.route("/search_topics", methods=['GET', 'POST'])
@login_required
def search_topics():
    image_file = url_for('static', filename='img/' + current_user.image_file)
    
    if request.method=='POST':
        book.key = request.form.get("q")
        
        # if log_manage.is_logged_in():
        #     username = log_manage.get_username()
        #     update_search_history(username, 'Topic', book.key)
        
        book.other_books = ol_subjects(book.key)
        if(len(book.other_books.keys())==0):
            flash("Sorry No Books",'error')
        book.book_stack["Recent"] = book.other_books
        return render_template('search.html', button="Topics", books=book.other_books, image_file=image_file)
    return render_template('search.html', button="Topics", books={}, image_file=image_file)



@auth.route("/bestsellers", methods=['GET', 'POST'])
def bestsellers():
    if request.method=='POST':
        book.key = request.form.get("q")
        book.other_books = ol_work_id(book.key)
        if(len(book.other_books.keys())==0):
            flash("Sorry No Books",'error')
        book.book_stack["Recent"] = book.other_books
        return render_template('bestsellers.html', books=book.other_books)
        
    return render_template('bestsellers.html', books={})


# additional helper function to load our individual user when trying to access protected routes
# telling Flask how to retrieve user using their id
@login_manager.user_loader
def load_user(id):
    """Check if user is logged-in upon page load."""
    if id is not None:
        return User.query.get(int(id)) # get will look for the primary key
    return None

# for catching authorization issues, calls unauthorized route anytime there are authorization issues
@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.', 'danger')
    return redirect(url_for('auth.login'))

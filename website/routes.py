from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_required, logout_user 
from bestsellers import *
from book_apis import *

main = Blueprint('main', __name__)

class Book:
    def __init__(self):
        self.key = ''
        self.other_books = {}
        self.home_search = ''
        self.book_stack = {"Recent":{},"Selected":{},"Favorite":{}}
        #self.image = icons[0][1]

book = Book()

# anyone who visits this page will see page
@main.route('/', methods=['GET', 'POST'])
def index():
  top_books, book.other_books = homepage_bestsellers()
  book.book_stack["Recent"] = book.other_books
  if request.method=='POST':
      book.key = request.form.get("q")
      book.other_books = ol_book_names(book.key)
      if(len(book.other_books.keys())==0):
          flash("Sorry No Books",'error')
      book.book_stack["Recent"] = book.other_books
      return render_template('books.html',button="Books", books=book.other_books, top_books=top_books)
  #### Return a rendered index.html file
  return render_template("index.html")

# You will also add route for adding notes here

# user cannot access this route unless their logged in
@main.route('/logout')
@login_required
def logout():
  logout_user()
  flash("You've been logged out", 'success')
  #### Return a rendered login.html file
  return redirect(url_for('auth.login'))

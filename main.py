from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
  
  #### Return a rendered index.html file
  return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

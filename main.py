from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
  
  #### Return a rendered index.html file
  return render_template("index.html")

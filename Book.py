from flask import Flask, render_template
from feed import generate_feed
from data_models import userdb, Post

app = Flask(__name__)

authed_user = "first"

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/feed')
def feed():
    return render_template('feed.html', feed = generate_feed(userdb[authed_user]), type=type, Post=Post)

@app.route('/profile')
def profile_user():
    return render_template('userprofile.html')

@app.route('/myorganization')
def profile_org():
    return render_template('orgprofile.html')

app.run()

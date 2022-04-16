from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/profile')
def profile_user():
    return render_template('userprofile.html')

@app.route('/myorganization')
def profile_org():
    return render_template('orgprofile.html')
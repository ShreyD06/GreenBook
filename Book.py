from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from feed import generate_feed
from data_models import userdb, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = '8472a8730b5c7742bedfdb29'


class RegisterForm(FlaskForm):
    username = StringField(label='User Name:')
    email_address = StringField(label='Email Address:')
    phone = StringField(label='Phone Number:')
    interests = StringField(label='Interests (Space Separated): ')
    password1 = PasswordField(label='Password:')
    password2 = PasswordField(label='Confirm Password:')
    submit = SubmitField(label='Create Account')

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(handle=form.username.data, email=form.email_address.data, phone_number=form.phone.data, interests=form.interests.data)
        return redirect(url_for('home_page'))
    return render_template('register.html', form=form)
    

@app.route('/settings')
def settings():
    return render_template('settings.html')
app.run()

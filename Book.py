from flask import Flask, render_template, redirect, url_for, request, make_response, after_this_request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from feed import generate_feed
from data_models import userdb, Post, User, Organization

app = Flask(__name__)
app.config['SECRET_KEY'] = '8472a8730b5c7742bedfdb29'

def authed_user():
    return request.cookies.get('user')

class RegisterForm(FlaskForm):
    username = StringField(label='User Name:')
    email_address = StringField(label='Email Address:')
    phone = StringField(label='Phone Number:')
    interests = StringField(label='Interests (Space Separated): ')
    password1 = PasswordField(label='Password:')
    password2 = PasswordField(label='Confirm Password:')
    submit = SubmitField(label='Create Account')

c = render_template
def render_template(path, *args, **kwargs):
    return c(path, *args, authed_user=authed_user(), **kwargs)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/feed')
def feed():
    return render_template('feed.html', feed = generate_feed(userdb[authed_user()]), type=type, Post=Post, User=User)

@app.route('/profile')
def profile_user():
    return render_template('userprofile.html')

@app.route('/myorganization')
def profile_org():
    org = Organization.get_from_admin(userdb[authed_user()])
    return render_template('orgprofile.html', name=org.name, desc=org.description, topics=org.topics, events=org.events)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_create = User(handle=form.username.data, email=form.email_address.data, phone_number=form.phone.data, interests=form.interests.data, password_hash=hash(form.password1.data))
        print("Added")
        return redirect(url_for('home_page'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        handle = request.form.get('name')
        password = request.form.get('password')
        print(handle, password)
        if User.auth(handle, password):
            @after_this_request
            def add_cookie(resp):
                resp.set_cookie('user', handle)
                return resp
            return redirect(url_for('home_page'))
        return 'submitted'
    return render_template('login.html')

@app.route('/logout')
def logout():
    @after_this_request
    def remove_cookie(resp):
        resp.set_cookie('user', '', max_age=0)
        return resp
    return redirect(url_for('home_page'))

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/sign_up_success')
def org_page():
    return render_template('orgprofile.html')

@app.route('/event_register/<eventid>', methods=['POST'])
def event_register(eventid):
    event = Event.from_id(eventid)
    user = authed_user()
    if user is not None:
        event.participants.append(userdb[user])

@app.route('/register_organization', methods=['POST'])
def register_organization():
    org = Organization(request.form.get('name'), userdb[authed_user()], request.form.get('description'))
    org.sync()
    return redirect(url_for('profile_org'))

# @app.route('/user/<handle>')
# def user_page(handle):
#     return render_template('user_page.html', handle = handle)

app.run(debug=True)

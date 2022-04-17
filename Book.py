from flask import Flask, render_template, redirect, url_for, request, make_response, after_this_request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from feed import generate_feed
from data_models import userdb, Post, User, Organization, Event, orgdb
from send_sms import send_sms
from datetime import date
from phash import phash

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
    if org is not None:
        return render_template('orgprofile.html', exists=True, org=org)
    else:
        return render_template('orgprofile.html', exists=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_create = User(handle=form.username.data, email=form.email_address.data, phone_number=form.phone.data, interests=form.interests.data, password_hash=phash(form.password1.data))
        user_create.sync()
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
    hours = request.form.get('hours')
    if user is not None:
        event.participants.append(userdb[user])
        send_sms(event.organization.admin.phone_number, user.name)

@app.route('/ars/<eventid>/<handle>/<hours>', methods=['POST'])
def ars(eventid, handle, hours):
    hours = int(hours)
    org = Organization.get_from_admin(userdb[authed_user()])
    user = userdb[handle]
    user.delta_rep(org, hours)
    org.delta_rep(user)
    ev = Event.from_id(eventid)
    ev.participants = [x for x in ev.participants if type(x) is tuple and x[0] != user]
    # ev.participants.remove((user, hours))   # FIXME
    ev.sync()
    orgdb.sync()
    return redirect(f'/event/{eventid}')

@app.route('/ars/decline/<eventid>/<handle>/<hours>', methods=['POST'])
def remove_hours(eventid, handle, hours):
    ev = Event.from_id(eventid)
    ev.participants.remove((userdb[handle], hours))     # FIXME
    return redirect(f'/event/{eventid}')

@app.route('/event/<eventid>')
def event_dashboard(eventid):
    # if authed_user() == Event.from_id(eventid).organization.admin:
    e = Event.from_id(eventid)
    new = []
    for x in e.participants:
        if type(x) is not tuple:
            new.append((x, 1))
        else:
            new.append(x)
    e.participants = new
    e.sync()
    orgdb.sync()
    return render_template('event_dashboard.html', ev = e, phash=phash)
    return 'not valid'

@app.route('/register_organization', methods=['POST'])
def register_organization():
    org = Organization(request.form.get('name'), userdb[authed_user()], request.form.get('description'))
    org.sync()
    return redirect(url_for('profile_org'))


@app.route('/topics')
def topics():
    return render_template('topics.html')

@app.route('/climate')
def Climate():
    return render_template('climate.html')

@app.route('/socialjustice')
def SocialJ():
    return render_template('socialj.html')


@app.route('/education')
def Education():
    return render_template('education.html')


@app.route('/animalwelfare')
def AnimalW():
    return render_template('animalwelfare.html')


@app.route('/disasterrelief')
def DisasterR():
    return render_template('disasterrelief.html')

@app.route('/post')
def Post():
    return render_template('make_post.html')

@app.route('/post-confirm', methods = ['GET', 'POST'])
def PConfirm():
    today = date.today()
    user = authed_user()
    post = Post(author=userdb[user], content=request.form.get('content'), date=today, tags=request.form.get('tags').split(' '))
    post.sync()
    postdb.sync()
    return redirect(url_for('home_page'))

@app.route('/post_event', methods = ['GET', 'POST'])
def PostEvent():
    return render_template('make_event.html')


@app.route('/event=confirm', methods = ['GET', 'POST'])
def EConfirm():
    event = Event(name=request.form.get('content'), organization=request.form.get('org'), participants=request.form.get('participants').split(' '))
    event.sync()
    orgdb.sync()
    return redirect(url_for('home_page'))
# @app.route('/user/<handle>')
# def user_page(handle):
#     return render_template('user_page.html', handle = handle)

app.run(debug=True)

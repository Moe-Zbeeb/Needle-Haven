import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from main_web.db import get_db
from flask_mail import Mail, Message
from main_web import mail
bp = Blueprint('auth', __name__, url_prefix='/auth')

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 
        email = request.form['email'] 
        first_name = request.form['first_name'] 
        last_name = request.form['last_name']   
        date_of_birth = request.form['date_of_birth'] 

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'  
        elif not email: 
            error = 'Email is required.' 
        elif not first_name: 
            error = 'First Name is required.' 
        elif not last_name: 
            error = 'Last Name is required.' 
        elif not date_of_birth: 
            error = 'Date of Birth is required.'  

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password_hash, email, first_name, last_name, date_of_birth) VALUES (?, ?, ?, ?, ?, ?)",
                    (username, generate_password_hash(password), email, first_name, last_name, date_of_birth),
                )
                db.commit()  
                send_welcome_email(email, username)
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')  


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password_hash'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')  

    

def send_welcome_email(to, username):
    msg = Message("Welcome to Our Service",
                  sender="your-email@example.com",
                  recipients=[to])
    msg.body = f"Hi {username},\n\nWelcome to chic! We're glad to have you with us.\n\nBest Regards,\nDev Team"
    mail.send(msg)
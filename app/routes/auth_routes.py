from flask import Blueprint, render_template, request, redirect, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re
from app.utils import get_logger

logger = get_logger(__name__)

bp = Blueprint('auth_routes', __name__)

"""
Authentication Routes:
- Handle user login
- Handle user account requests
- Handle user logout
"""

@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        logger.debug("Login attempt received for user: %s", username)

        db = current_app.get_db()
        user = db.execute("SELECT * FROM User WHERE UserName = ?", (username,)).fetchone()

        if user:
            if not user['Account_Active']:
                logger.warning("Inactive account attempted login: %s", username)
                return render_template("login.html", error="Account not active.")

            if check_password_hash(user['Password'], password):
                logger.info("Successful login: %s", username)
                session['user'] = username
                session.permanent = True
                db.execute("UPDATE User SET Last_Login_Date = ?, Num_Login_attempts = 0 WHERE id = ?",
                           (datetime.now(), user['id']))
                db.commit()
                return redirect('/jump')
            else:
                logger.warning("Failed login (bad password): %s", username)
                db.execute("UPDATE User SET Num_Login_attempts = Num_Login_attempts + 1 WHERE id = ?",
                           (user['id'],))
                db.commit()
        else:
            logger.warning("Failed login (unknown user): %s", username)

    return render_template('login.html')

@bp.route('/request_access', methods=['GET', 'POST'])
def request_access():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not is_strong_password(password):
            error = "Password must be at least 8 characters and include letters, numbers, and special characters."
            return render_template('request_access.html', error=error)

        db = current_app.get_db()
        existing = db.execute("SELECT * FROM User WHERE UserName = ?", (username,)).fetchone()

        if not existing:
            now = datetime.now()
            db.execute("INSERT INTO User (UserName, Password, Date_Created, Last_Login_Date, Last_PWD_Reset, Num_Login_attempts, has_Admin, Account_Active) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",(username, generate_password_hash(password), now, now, now, 0, 0, 0))
            print(f"Added {username}")
            db.commit()
            return redirect('/')
        else:
            error = "Username already exists."

    return render_template('request_access.html', error=error)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')

def is_strong_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Za-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

from flask import Blueprint, render_template, request, redirect, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

bp = Blueprint('auth_routes', __name__)

@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = current_app.get_db()
        user = db.execute(\"SELECT * FROM User WHERE UserName = ?\", (username,)).fetchone()

        if user and check_password_hash(user['Password'], password) and user['Account_Active']:
            session['user'] = username
            db.execute(\"\"\"UPDATE User SET Last_Login_Date = ?, Num_Login_attempts = 0 WHERE id = ?\"\"\",
                       (datetime.now(), user['id']))
            db.commit()
            return redirect('/jump')
        elif user:
            db.execute(\"\"\"UPDATE User SET Num_Login_attempts = Num_Login_attempts + 1 WHERE id = ?\"\"\", (user['id'],))
            db.commit()

    return render_template('login.html')

@bp.route('/request_access', methods=['GET', 'POST'])
def request_access():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = current_app.get_db()
        existing = db.execute(\"SELECT * FROM User WHERE UserName = ?\", (username,)).fetchone()

        if not existing:
            now = datetime.now()
            db.execute(\"\"\"INSERT INTO User (UserName, Password, Date_Created, Last_Login_Date,
                        Last_PWD_Reset, Num_Login_attempts, has_Admin, Account_Active)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)\"\"\",
                        (username, generate_password_hash(password), now, now, now, 0, 0, 0))
            db.commit()
            return redirect('/')
    return render_template('request_access.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')

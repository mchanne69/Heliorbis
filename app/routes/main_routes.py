from flask import Blueprint, render_template, session, redirect, current_app

bp = Blueprint('main_routes', __name__)

@bp.route('/jump')
def jump():
    if 'user' not in session:
        return redirect('/')

    db = current_app.get_db()
    user = db.execute("SELECT * FROM User WHERE UserName = ?", (session['user'],)).fetchone()
    is_admin = user and user['has_Admin']
    return render_template('jump_page.html', user=session['user'], is_admin=is_admin)
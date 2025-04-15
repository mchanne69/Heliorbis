from flask import Blueprint, render_template, session, redirect

bp = Blueprint('main_routes', __name__)

@bp.route('/jump')
def jump():
    if 'user' not in session:
        return redirect('/')
    return render_template('jump_page.html', user=session['user'])

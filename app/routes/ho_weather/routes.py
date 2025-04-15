from flask import Blueprint, render_template, session, redirect

bp = Blueprint('weather_routes', __name__, url_prefix='/weather')

@bp.route('/')
def weather_home():
    if 'user' not in session:
        return redirect('/')
    return render_template('apps/ho_weather.html')

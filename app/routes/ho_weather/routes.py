from flask import Blueprint, render_template, request, current_app
import requests

bp = Blueprint('weather_routes', __name__, url_prefix='/weather', template_folder='templates')

DEFAULT_LAT = 28.1939
DEFAULT_LON = -82.5918

@bp.route('/', methods=['GET', 'POST'])
def weather():
    lat = request.form.get('lat', DEFAULT_LAT)
    lon = request.form.get('lon', DEFAULT_LON)
    unit_type = 'imperial'
    error = None
    weather_data = None

    try:
        api_key = current_app.config['OW_API_KEY']
        if not api_key:
            raise ValueError("API key not configured.")

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={unit_type}"
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
    except Exception as e:
        error = f"Error fetching weather data: {e}"

    return render_template('ho_weather.html', weather=weather_data, lat=lat, lon=lon, error=error)

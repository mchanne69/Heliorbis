from flask import Blueprint, render_template, request, current_app, flash
import requests
from app.routes.ho_weather.utils import generate_wind_compass_image

bp = Blueprint('weather_routes', __name__, url_prefix='/weather', template_folder='templates')

DEFAULT_LAT = 28.1939
DEFAULT_LON = -82.5918

"""
Weather Module Routes:
- Fetch current weather from OpenWeather API
- Display weather data to users
- Allow user input of custom latitude/longitude
"""

@bp.route('/', methods=['GET', 'POST'])
def weather():
    lat = request.form.get('lat', DEFAULT_LAT)
    lon = request.form.get('lon', DEFAULT_LON)
    unit_type = 'imperial'
    error = None
    weather_data = None
    wind_label = None
    wind_img_path = 'static/images/wind_dir.png'


    try:
        api_key = current_app.config['OW_API_KEY']
        if not api_key:
            raise ValueError("API key not configured.")

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={unit_type}"
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()

        if 'wind' in weather_data and 'deg' in weather_data['wind']:
            wind_deg = weather_data['wind']['deg']
            wind_label = generate_wind_compass_image(wind_deg, f'app/{wind_img_path}')

    except Exception as e:
        flash(f"Error fetching weather data: {e}", "error")

    return render_template('ho_weather.html', weather=weather_data, lat=lat, lon=lon, error=error,
                           wind_label=wind_label, wind_img=wind_img_path if wind_label else None)
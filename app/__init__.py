from flask import Flask
import os
from app.database import init_db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'replace_this_with_a_real_secret'
    app.config['DATABASE'] = os.path.join(os.getcwd(), 'HO_admin.sqlite')

    init_db(app)

    from app.routes import auth_routes, main_routes
    from app.routes.ho_weather import routes as weather_routes

    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(main_routes.bp)
    app.register_blueprint(weather_routes.bp)

    return app

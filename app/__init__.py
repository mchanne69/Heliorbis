from flask import Flask
from app.database import init_db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)

    from app.routes import auth_routes, main_routes
    from app.routes.ho_admin import routes as admin_routes
    from app.routes.ho_weather import routes as weather_routes

    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(main_routes.bp)
    app.register_blueprint(admin_routes.bp)
    app.register_blueprint(weather_routes.bp)

    return app

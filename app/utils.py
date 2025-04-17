import logging
from flask import current_app, session, redirect
from functools import wraps
import os
from logging.handlers import RotatingFileHandler

def get_logger(name='app'):
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        log_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, 'app.log')

        handler = RotatingFileHandler(log_path, maxBytes=500000, backupCount=3)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        try:
            app_debug = current_app.config.get('APP_DEBUG', False)
            logger.setLevel(logging.DEBUG if app_debug else logging.WARNING)
        except RuntimeError:
            logger.setLevel(logging.WARNING)

    return logger

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        db = current_app.get_db()
        username = session.get('user')
        if not username:
            return redirect('/')
        user = db.execute("SELECT has_Admin FROM User WHERE UserName = ?", (username,)).fetchone()
        if not user or not user['has_Admin']:
            return redirect('/jump')
        return view_func(*args, **kwargs)
    return wrapper
import os
from dotenv import load_dotenv

# Load .env into the environment
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-insecure-dev-key")

    # Allow override via .env, but fallback to path-relative SQLite
    DATABASE = os.getenv("DATABASE")

    if not os.path.isabs(DATABASE):
        DATABASE = os.path.join(basedir, DATABASE)

    APP_DEBUG = os.getenv('APP_DEBUG', 'False').lower() in ['1', 'true', 'yes']

    OW_API_KEY = os.getenv('OW_API_KEY')

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # change to True in production with HTTPS
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes



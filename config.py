import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'replace_this_with_a_real_secret'
    DATABASE = os.path.join(basedir, 'HO_admin.sqlite')

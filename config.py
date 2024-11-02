"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv
from datetime import timedelta
from sys import platform


basedir = path.abspath(path.dirname(__file__))
if platform.startswith('dar'):
    load_dotenv(path.join(basedir, 'mac.env'))
else:
    load_dotenv(path.join(basedir, '.env'))

__all__ = ['Config']

class Config:
    """Set Flask config variables."""

    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = environ.get('SECRET_KEY')
    WEBSITE_NAME = "BlueTemp"
    print(WEBSITE_NAME)
    WEBSITE_EMAIL = environ.get("WEBSITE_EMAIL")
    WEBSITE_LOGO = environ.get("WEBSITE_LOGO")
    HOMEPAGE_ABOUT = environ.get("HOMEPAGE_ABOUT")

    TEMPLATES_FOLDER = 'templates'
    ADDRESS = environ.get('ADDRESS')
    DB_PASSWORD = environ.get("DB_PASSWORD")

    # Database
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+environ.get('MYSQL_ROOT_USER')+':'+environ.get('MYSQL_ROOT_PASSWORD')+'@'+environ.get('HOST')+':'+environ.get('DB_PORT')+'/'+environ.get('DB')

    JWT_SECRETE_KEY = environ.get('JWT_SECRETE_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_ENGINE_OPTIONS = {
                                 'pool_size' : 10,
                                 'pool_recycle':120,
                                 'pool_pre_ping': True,
                                 'max_overflow': 5
                                 }

    # Session related config
    SESSION_PERMANENT = True
    SESSION_TYPE = "filesystem"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=5)

    # Database gone away fix
    SQLALCHEMY_POOL_PRE_PING =True


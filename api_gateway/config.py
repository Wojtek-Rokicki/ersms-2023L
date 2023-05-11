

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Flask application secret
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24).hex()
    # Database access
    SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRES_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Google's OAuth2
    OAUTH_GOOGLE_CLIENT_ID=os.environ.get('OAUTH_GOOGLE_CLIENT_ID')
    OAUTH_GOOGLE_CLIENT_SECRET=os.environ.get('OAUTH_GOOGLE_CLIENT_SECRET')
    OAUTH_GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )
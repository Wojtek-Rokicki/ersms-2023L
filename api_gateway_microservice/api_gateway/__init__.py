
# Third-party libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from oauthlib.oauth2 import WebApplicationClient

# Internal imports
from api_gateway.config import Config

server = Flask(__name__)
server.config.from_object(Config)

db = SQLAlchemy(server)
migrate = Migrate(server, db)
login = LoginManager(server)

# OAuth 2 client setup
client = WebApplicationClient(server.config['OAUTH_GOOGLE_CLIENT_ID'])

from api_gateway import routes, models

with server.app_context():
    db.create_all()
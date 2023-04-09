import os, json, jwt
from flask import Flask, request, url_for, render_template, redirect, session
from flask_mysqldb import MySQL
from authlib.integrations.flask_client import OAuth

server = Flask(__name__)
server.secret_key='random secret' # random hash on deployment

# oauth config
oauth = OAuth(server)
oauth.register(
    name='google',
    client_id=os.environ.get('OAUTH_GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('OAUTH_GOOGLE_CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',    
    client_kwargs={'scope': 'profile email'}, # removed openid
)

@server.route("/", methods=["GET"])
def hello_world():
    email = dict(session).get('email', None)
    return f"Hello {email}!"

@server.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@server.route('/authorize')
def authorize():
    token = oauth.google.authorize_access_token()
    resp = oauth.google.get('userinfo')
    user_info = resp.json()
    # do something with the token and profile
    session['email'] = user_info['email']
    return redirect('/')

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
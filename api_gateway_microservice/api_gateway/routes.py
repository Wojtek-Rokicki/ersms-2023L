import requests, json, sys, os

from flask import Flask, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)


from api_gateway.config import Config
from api_gateway import server, db, client
from api_gateway.models import User

def get_google_provider_cfg():
    return requests.get(server.config['OAUTH_GOOGLE_DISCOVERY_URL']).json()


@server.route("/", methods=["GET"])
def index():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'

@server.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@server.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(server.config['OAUTH_GOOGLE_CLIENT_ID'], server.config['OAUTH_GOOGLE_CLIENT_SECRET']),
    )

    # Parse the tokens
    client.parse_request_body_response(json.dumps(token_response.json()))

    # URL from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
        users_surname = userinfo_response.json()["family_name"]
    else:
        return "User email not available or not verified by Google.", 400

    user = User.query.filter_by(email=users_email).first()

    if user is None:
        print("Registering new user", file=sys.stderr)
        user = User(
            google_id=unique_id, name=users_name, surname=users_surname, email=users_email, profile_pic=picture
        )
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    
    return redirect(url_for("index"))

@server.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

def forward_request(api_endpoint_address, api_endpoint_name):
    response = requests.get(
        f"http://{os.environ.get(api_endpoint_address)}/{api_endpoint_name}"
    )
    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
    
@server.route('/restricted_access', methods=["GET"])
@login_required
def restricted_access():
    return "Authorized access"


@server.route('/users', methods=["GET"])
@login_required
def users():
    content, err = forward_request("MIDDLEWARE_ADDRESS", "users")
    return "Authorized access"

@server.route('/friends', methods=["GET"])
@login_required
def friends():
    content, err = forward_request("MIDDLEWARE_ADDRESS", "friends")
    return "Authorized access"

@server.route('/events', methods=["GET"])
@login_required
def events():
    content, err = forward_request("MIDDLEWARE_ADDRESS", "events")
    return "Authorized access"

@server.route('/activities', methods=["GET"])
@login_required
def activities():
    content, err = forward_request("MIDDLEWARE_ADDRESS", "activities")
    return "Authorized access"

@server.route('/signups', methods=["GET"])
@login_required
def signups():
    content, err = forward_request("MIDDLEWARE_ADDRESS", "signups")
    return "Authorized access"
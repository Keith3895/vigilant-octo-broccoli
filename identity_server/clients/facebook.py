from flask import Flask, url_for, session, g, Blueprint, current_app
from flask import render_template, redirect
from authlib.integrations.flask_client import OAuth
from .utils import saveToken, linkedin_account_mapper

bp = Blueprint(__name__, 'client', url_prefix='/auth/facebook/')

# app.config.from_object('config')

# CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(current_app)


@bp.route('/login')
def login():
    oauth.register(
        name='facebook',
        # server_metadata_url=CONF_URL,
        client_id=current_app.config['FACEBOOK_CLIENT_ID'],
        client_secret=current_app.config['FACEBOOK_CLIENT_SECRET'],
        api_base_url='https://graph.facebook.com/v10.0/',
        access_token_url='https://graph.facebook.com/v10.0/oauth/access_token',
        authorize_url='https://www.facebook.com/v10.0/dialog/oauth',
        client_kwargs={
            'scope': 'email public_profile user_photos'
        }
    )
    redirect_uri = url_for('.auth', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)


@bp.route('/auth')
def auth():
    token = oauth.facebook.authorize_access_token()
    print(token)
    resp = oauth.facebook.get('https://graph.facebook.com/me')
    me = resp.json()
    resp_user = oauth.facebook.get('https://graph.facebook.com/'+me['id']+'?fields=email,name,first_name,last_name')
    user = resp_user.json()
    print("user")
    print(user)
    userObject = facebook_account_mapper(user)
    saveToken(token, userObject)
    return redirect('/')


# @bp.route('/logout')
# def logout():
#     session.pop('user', None)
#     return redirect('/')

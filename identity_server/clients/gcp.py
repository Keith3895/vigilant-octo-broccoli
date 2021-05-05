from flask import Flask, url_for, session, g, Blueprint, current_app, request
from flask import render_template, redirect
from authlib.integrations.flask_client import OAuth
from .utils import gcp_account_mapper, saveToken
from identity_server.provider.oauth2 import authorization
from authlib.oauth2 import OAuth2Request

bp = Blueprint(__name__, 'client', url_prefix='/auth/gcp/')

# app.config.from_object('config')

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(current_app)


@bp.route('/login')
def login():
    oauth.register(
        name='google',
        server_metadata_url=CONF_URL,
        client_id=current_app.config['GCP_CLIENT_ID'],
        client_secret=current_app.config['GCP_CLIENT_SECRET'],
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    redirect_uri = url_for('.auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@bp.route('/auth')
def auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    userObject = gcp_account_mapper(user)
    saveToken(token, userObject)
    return redirect(url_for('identity_server.provider.routes.authorize', user=userObject.id,
                            response_type='code', client_id='D23YEFyX9HZxhj0G3uUKerJZ', scope='profile'
                            ))
    # return redirect('foobar://success?code='+token['access_token'])


# @bp.route('/logout')
# def logout():
#     session.pop('user', None)
#     return redirect('/')

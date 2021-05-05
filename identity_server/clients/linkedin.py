from flask import Flask, url_for, session, g, Blueprint, current_app
from flask import render_template, redirect
from authlib.integrations.flask_client import OAuth
from .utils import saveToken, linkedin_account_mapper

bp = Blueprint(__name__, 'client', url_prefix='/auth/linkedin/')

# app.config.from_object('config')

# CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(current_app)


@bp.route('/login')
def login():
    oauth.register(
        name='linkedin',
        # server_metadata_url=CONF_URL,
        client_id=current_app.config['LINKEDIN_CLIENT_ID'],
        client_secret=current_app.config['LINKEDIN_CLIENT_SECRET'],
        api_base_url='https://api.linkedin.com/v2/',
        access_token_url='https://www.linkedin.com/oauth/v2/accessToken',
        authorize_url='https://www.linkedin.com/oauth/v2/authorization',
        client_kwargs={
            'scope': 'r_liteprofile r_emailaddress'
        }
    )
    redirect_uri = url_for('.auth', _external=True)
    return oauth.linkedin.authorize_redirect(redirect_uri)


@bp.route('/auth')
def auth():
    token = oauth.linkedin.authorize_access_token()
    url = 'me'
    resp = oauth.linkedin.get(url)
    user = resp.json()
    url = 'emailAddress?q=members&projection=(elements*(handle~))'
    email_resp = oauth.linkedin.get(url)
    email = email_resp.json()
    userObject = linkedin_account_mapper(user, email)
    saveToken(token, userObject)
    return redirect(url_for('identity_server.provider.routes.authorize', user=userObject.id,
                            response_type='code', client_id='D23YEFyX9HZxhj0G3uUKerJZ', scope='profile'
                            ))


# @bp.route('/logout')
# def logout():
#     session.pop('user', None)
#     return redirect('/')

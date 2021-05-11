from flask import Flask, url_for, session, g, Blueprint, current_app,request,jsonify
from flask import render_template, redirect
from authlib.integrations.flask_client import OAuth
from .utils import saveToken, facebook_account_mapper
from identity_server.models import OAuth2Client, OAuth2Providers
from sqlalchemy import and_
from identity_server.utils import AlchemyEncoder
import json
bp = Blueprint(__name__, 'client', url_prefix='/auth/facebook/')

# app.config.from_object('config')

# CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(current_app)


@bp.route('/login')
def login():
    req_clientId = request.args.get('clientId')
    req_clientSecret = request.args.get('clientSecret')
    if not req_clientId or not req_clientSecret:
        return 'client credentials not provided.'
    result = OAuth2Client.query.filter(and_(
        OAuth2Client.client_id == req_clientId, OAuth2Client.client_secret == req_clientSecret))\
        .join(OAuth2Providers, OAuth2Client.id == OAuth2Providers.local_client_id)\
        .with_entities(OAuth2Providers.client_id, OAuth2Providers.client_secret)\
        .filter(OAuth2Providers.provider_id == 3).first()
    oauth.register(
        name='facebook',
        # server_metadata_url=CONF_URL,
        client_id=result[0],
        client_secret=result[1],
        api_base_url='https://graph.facebook.com/v10.0/',
        access_token_url='https://graph.facebook.com/v10.0/oauth/access_token',
        authorize_url='https://www.facebook.com/v10.0/dialog/oauth',
        client_kwargs={
            'scope': 'email public_profile user_photos'
        }
    )
    redirect_uri = url_for('.auth', _external=True)
    session['client'] = str(dict(client_id=result[0],
                                 client_secret=result[1],req_clientId=req_clientId))
    return oauth.facebook.authorize_redirect(redirect_uri)


@bp.route('/auth')
def auth():
    clientConfig = eval(session['client'])
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
    return redirect(url_for('identity_server.provider.routes.authorize', user=userObject.id,
                            response_type='code', client_id=clientConfig.get('req_clientId'), scope='profile'
                            ))


# @bp.route('/logout')
# def logout():
#     session.pop('user', None)
#     return redirect('/')

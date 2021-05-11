from flask import Flask, url_for, session, g, Blueprint, current_app, request, Response
from flask import render_template, redirect, jsonify
from authlib.integrations.flask_client import OAuth
from .utils import gcp_account_mapper, saveToken
from identity_server.provider.oauth2 import authorization
from authlib.oauth2 import OAuth2Request
from identity_server.models import OAuth2Client, OAuth2Providers
from sqlalchemy import and_
from identity_server.utils import AlchemyEncoder
import json

bp = Blueprint(__name__, 'client', url_prefix='/auth/gcp/')

# app.config.from_object('config')

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
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
        .filter(OAuth2Providers.provider_id == 1).first()
    if not result:
        return jsonify(message="client config not found."), 406
    print(result[0])
    oauth.register(
        name='google',
        server_metadata_url=CONF_URL,
        client_id=result[0],
        client_secret=result[1],
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    redirect_uri = url_for('.auth', _external=True)
    session['client'] = str(dict(client_id=result[0],
                                 client_secret=result[1],req_clientId=req_clientId))
    return oauth.google.authorize_redirect(redirect_uri)


@bp.route('/auth')
def auth():
    clientConfig = eval(session['client'])
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    userObject = gcp_account_mapper(user)
    saveToken(token, userObject)
    session.get('client')
    print(session['client'])
    return redirect(url_for('identity_server.provider.routes.authorize', user=userObject.id,
                            response_type='code', client_id=clientConfig.get('req_clientId'), scope='profile'
                            ))
    # return redirect('foobar://success?code='+token['access_token'])


# @bp.route('/logout')
# def logout():
#     session.pop('user', None)
#     return redirect('/')

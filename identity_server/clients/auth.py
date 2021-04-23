import functools
from flask import session, current_app, Blueprint, g, redirect, session, url_for, request, make_response, jsonify
from identity_server.db import get_db
from requests_oauthlib import OAuth2Session
bp = Blueprint('auth', __name__, url_prefix='/auth')

scope = ['https://www.googleapis.com/auth/userinfo.email',
         'https://www.googleapis.com/auth/userinfo.profile', 'openid']


@bp.route('/gcp/login', methods=('GET', 'POST'))
def gcp_login():
    if request.method == 'GET':

        if request.args.get('redirect_uri') != None:
            session['redirect_uri'] = request.args.get('redirect_uri')

        # return jsonify({'result': [dict(row) for row in res]})
        return redirect(generate_auth_url())
    else:
        return 'error'


@bp.route('/gcp/login/cb', methods=('GET', 'POST'))
def gcp_login_callback():
    oauth, client_id, client_secret = init_oauth()
    if request.method == 'GET':
        authorization_response = request.url
        session['token'] = oauth.fetch_token('https://accounts.google.com/o/oauth2/token',
                                             authorization_response=authorization_response,
                                             client_secret=client_secret)
        print(session)
        return redirect(session['redirect_uri'])

@bp.route('/token')
def getToken():
    return session['token']

def generate_auth_url():
    oauth, client_id, client_secret = init_oauth()
    authorization_url, state = oauth.authorization_url(
        'https://accounts.google.com/o/oauth2/auth',
        # access_type and prompt are Google specific extra
        # parameters.
        access_type="offline", prompt="select_account")
    return authorization_url


def init_oauth():
    client_id = current_app.config['GCP_CLIENT_ID']
    client_secret = current_app.config['GCP_CLIENT_SECRET']
    redirect_uri = current_app.config['HOST_NAME'] + \
        url_for('auth.gcp_login_callback')
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,
                          scope=scope)
            
    return (oauth, client_id, client_secret)

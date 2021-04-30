from identity_server.models import db, User, OAuth2Token


def gcp_account_mapper(gcp_user):
    user = User.query.filter_by(email=gcp_user.email).first()
    if not user:
        user = User(
            username=gcp_user.email,
            email=gcp_user.email,
            full_name=gcp_user.name,
            first_name=gcp_user.given_name,
            last_name=gcp_user.family_name,
            profile_picture=gcp_user.picture
        )
        db.session.add(user)
        db.session.commit()
    return user

def facebook_account_mapper(facebook):
    user = User.query.filter_by(email=facebook.email).first()
    if not user:
        user = User(
            username=facebook.email,
            email=facebook.email,
            full_name=facebook.name,
            first_name=facebook.given_name,
            last_name=facebook.family_name
        )
        db.session.add(user)
        db.session.commit()
    return user

def saveToken(token, user):
    if 'id_token' in token:
        token.pop('id_token')
    if 'expires_at' in token:
        token.pop('expires_at')
    oauth_token = OAuth2Token(
        user_id=user.id,
        **token
    )
    db.session.add(oauth_token)
    db.session.commit()


def linkedin_account_mapper(linkedin_user, email_obj):
    email = email_obj['elements'][0]['handle~']['emailAddress']
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            username=email,
            email=email,
            full_name=linkedin_user['localizedFirstName']+" "+linkedin_user['localizedLastName'],
            first_name=linkedin_user['localizedFirstName'],
            last_name=linkedin_user['localizedLastName']
        )
        db.session.add(user)
        db.session.commit()
    return user

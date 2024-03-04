from flask import jsonify, url_for
from flask_jwt_extended import create_access_token

from intelli_scan.resource.oauth import oauth_bp, oauth
from intelli_scan.database.models.user import UserModel as User


# OAuth callback route
@oauth_bp.route('/api/google/auth/callback', endpoint='google-login-callback', methods=['GET'])
def google_callback():
    token = oauth.google.authorize_access_token()

    # Check if the user already exists in the database
    user = User.query.filter_by(
        google_id=token['userinfo']['sub']).first()
    if not user:
        # Create a new user in the local database
        user = User(
            email=token['userinfo']['email'],
            name=f"{token['userinfo']['given_name']} {token['userinfo']['family_name']}",
            google_id=token['userinfo']['sub']
        )
        user.save_to_db()

    # Generate a JWT token for the user
    auth_token = create_access_token(identity=user.id)
    return jsonify(user_id=user.id, message=f'Logged in as {user.name}', auth_token=auth_token)


# OAuth login route
@oauth_bp.route('/api/google/login/callback', endpoint='google-login', methods=['GET'])
def google_login():
    redirect_uri = url_for('oauth.google-login-callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

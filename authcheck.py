"""
This module handles authentications
"""
import json
from functools import wraps
import http.client
from flask import Flask, request, _request_ctx_stack
from flask.json import jsonify
from jose import jwt
from six.moves.urllib.request import urlopen
import db # pylint: disable=import-error

AUTH0_DOMAIN = 'dev-2ajo016m.us.auth0.com'
API_AUDIENCE = 'https://smart_bookmarks/api'
ALGORITHMS = ["RS256"]
app = Flask(__name__)

class AuthError(Exception):
    """
    Handles auth related errors
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    """
    Handles authorization related errors
    """
    res = jsonify(ex.error)
    res.status_code = ex.status_code
    return res


# Format error response and append status code
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token


def requires_auth(func):
    """
    Determines if the Access Token is valid
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError as err:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401) from err
            except jwt.JWTClaimsError as err:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    "please check the audience and issuer"}, 401) from err
            except Exception as err:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401) from err

            _request_ctx_stack.top.current_user = payload
            return func(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated


def validate_user(user_id, password):
    """
    check if user is valid
    return access token as an object if user is valid
    raise auth error otherwise
    """

    user_is_valid = db.is_valid_user(user_id, password)

    print("is user valid? - ", user_is_valid)

    if user_is_valid:
        try:
            conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
            payload = "{\"client_id\":\"vlKnFcLWHhA16V6DUZbcOzXyGlfVuXN0\",\"client_secret\":\"9zgdj5UoxvbcySR1Z0bVvOGOGEjQAIfc57h3LrsSGDxmROTkOJ_oJU_jqZuf7_tJ\",\"audience\":\"https://smart_bookmarks/api\",\"grant_type\":\"client_credentials\"}" # pylint: disable=line-too-long

            headers = { 'content-type': "application/json" }
            conn.request("POST", "/oauth/token", payload, headers)

            print("connection established and request sent")

            # If all goes well, you'll receive an HTTP 200 response
            # with a payload containing access_token, token_type,
            # and expires_in values:
            # {
            # "access_token":"eyJz93a...k4laUWw",
            # "token_type":"Bearer",
            # "expires_in":86400
            # }
            res = conn.getresponse()
            data = res.read().decode("utf-8")
            json_data = json.loads(data)
            print("data received")

            # tie the access token to this user
            db.update_token(user_id, password, json_data['access_token'])

            return json_data

        except Exception: #as err:
            return None
            # raise AuthError({"code": "HTTP_request_error",
            #                 "description":
            #                     "Unable to get response from domain"}, 401) from err
    return None
    # raise AuthError({"code": "invalid_user",
    #                 "description": "Invalid user_id and password combination"}, 401)

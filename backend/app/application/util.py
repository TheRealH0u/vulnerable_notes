import os, jwt, datetime
from flask import jsonify, abort, session, url_for, redirect, request
from functools import wraps


generate = lambda x: os.urandom(x).hex()
key = 'SOtqCasVL3Icp0fBOiFg5W2YdvgkqKrpki0nXzdKUUWKTSigK0'


def response(message):
    return jsonify({'message': message})


def createJWT(username):
    token_expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=360)
    encoded = jwt.encode(
        {
            'username': username,
            'exp': token_expiration
        },
        key,
        algorithm='HS256'
    )
    return encoded


def verifyJWT(token):
    try:
        token_decode = jwt.decode(
            token,
            key,
            algorithms=['HS256']
        )
        return token_decode
    except:
        return abort(400, 'Invalid token!')


def authenticated(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return redirect(url_for('web.login'))
        verifyJWT(token)
        return f(*args, **kwargs)
    return decorator


def isAdmin(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = verifyJWT(request.cookies.get('token'))
        if token and token['username'] == 'admin':
            return f(*args, **kwargs)
        else:
            return abort(401, 'Unauthorised access detected!')
    return decorator

def isAdminBool():
    #Checks if user is admin using JWT token and return a bool value of False or True
    token = verifyJWT(request.cookies.get('token'))
    if token and token['username'] == 'admin':
        return True
    else:
        return False

def getUsername():
    """
    Returns the username from the JWT token in the request cookies.
    If no valid token is present, returns None.
    """
    token = request.cookies.get('token')
    if not token:
        return None
    try:
        decoded = verifyJWT(token)
        return decoded.get('username')
    except:
        return None


def slugify_title(title: str) -> str:
    """
    Convert a note title into a URL-friendly slug.

    Examples:
    - "Hello World!" -> "hello-world"
    - "  New: Note/Title " -> "new-note-title"

    This function lowercases the string, replaces any sequence of
    non-alphanumeric characters with a single hyphen, and strips
    leading/trailing hyphens.
    """
    if not isinstance(title, str):
        raise TypeError('title must be a string')

    # Normalize to ASCII equivalent where possible
    try:
        import unicodedata
        title = unicodedata.normalize('NFKD', title)
        title = title.encode('ascii', 'ignore').decode('ascii')
    except Exception:
        # If anything goes wrong with normalization, fall back to original
        pass

    # Replace non-alphanumeric sequences with hyphens
    import re
    slug = re.sub(r"[^a-zA-Z0-9]+", '-', title.lower()).strip('-')
    return slug

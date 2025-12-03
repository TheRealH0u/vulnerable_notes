from flask import Blueprint, request, jsonify, make_response, redirect
from application.models import Users, Note, db
from application.util import createJWT, verifyJWT
from werkzeug.security import check_password_hash, generate_password_hash

api = Blueprint('api', __name__)


def token_username():
    token = request.cookies.get('token') or request.headers.get('Authorization')
    if not token:
        return None
    if token.startswith('Bearer '):
        token = token.split(' ',1)[1]
    try:
        decoded = verifyJWT(token)
        return decoded.get('username')
    except:
        return None


@api.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error':'missing'}), 400
    user = Users.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error':'invalid'}), 401
    token = createJWT(user.username)
    resp = make_response(jsonify({'message':'ok'}))
    resp.set_cookie('token', token, path='/', httponly=False, secure=False)
    return resp


@api.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    verify = data.get('verify')
    if not (username and email and password and verify):
        return jsonify({'error':'missing'}), 400
    if password != verify:
        return jsonify({'error':'mismatch'}), 400
    if Users.query.filter_by(username=username).first():
        return jsonify({'error':'user_exists'}), 400
    if Users.query.filter_by(email=email).first():
        return jsonify({'error':'email_exists'}), 400
    user = Users(username=username, email=email, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return jsonify({'message':'created'}), 201


@api.route('/api/settings', methods=['POST'])
def api_settings():
    username = token_username()
    if not username:
        return jsonify({'error':'unauthenticated'}), 401
    data = request.get_json() or {}
    password = data.get('password')
    if not password:
        return jsonify({'error':'missing'}), 400
    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error':'no_user'}), 400
    user.password = generate_password_hash(password)
    db.session.commit()
    return jsonify({'message':'updated'})


@api.route('/api/notes', methods=['GET'])
def api_notes():
    username = token_username()
    if not username:
        return jsonify({'error':'unauthenticated'}), 401
    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({'notes':[]})
    notes = [
        {
            'id': n.id,
            'title': n.title,
            'content': n.content,
            'created_at': n.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        for n in Note.query.filter_by(user_id=user.id).order_by(Note.id).all()
    ]
    return jsonify({'notes': notes})


@api.route('/api/notes', methods=['POST'])
def api_create_note():
    username = token_username()
    if not username:
        return jsonify({'error':'unauthenticated'}), 401
    data = request.get_json() or {}
    title = data.get('title') or ''
    content = data.get('content') or ''
    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error':'no_user'}), 400
    note = Note(title=title, content=content, user_id=user.id)
    db.session.add(note)
    db.session.commit()
    return jsonify({'message':'created','id':note.id}), 201


@api.route('/api/notes/<int:note_id>', methods=['PUT','DELETE'])
def api_note_modify(note_id):
    username = token_username()
    if not username:
        return jsonify({'error':'unauthenticated'}), 401
    user = Users.query.filter_by(username=username).first()
    note = Note.query.filter_by(id=note_id, user_id=user.id).first()
    if not note:
        return jsonify({'error':'not_found'}), 404
    if request.method == 'DELETE':
        db.session.delete(note)
        db.session.commit()
        return jsonify({'message':'deleted'})
    data = request.get_json() or {}
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)
    db.session.commit()
    return jsonify({'message':'updated'})


@api.route('/logout', methods=['GET'])
def api_logout():
    # Clear the token cookie and redirect to the login page (frontend will handle the route)
    resp = make_response(redirect('/login'))
    resp.delete_cookie('token', path='/')
    return resp


@api.route('/api/me', methods=['GET'])
def api_me():
    username = token_username()
    if not username:
        return jsonify({'error':'unauthenticated'}), 401
    return jsonify({'username': username})


@api.route('/api/user', methods=['GET'])
def api_user():
    username = token_username()
    if not username:
        return jsonify({'error':'unauthenticated'}), 401
    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error':'no_user'}), 404
    return jsonify({'username': user.username, 'email': user.email})


@api.route('/api/logout', methods=['POST','GET'])
def api_logout_json():
    # Clear token cookie and return JSON. Use for SPA logout through /api/* proxy.
    resp = make_response(jsonify({'message':'logged_out'}))
    resp.delete_cookie('token', path='/')
    return resp

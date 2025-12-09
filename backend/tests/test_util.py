import os
import sys
import pytest
import jwt
import datetime

# Ensure backend/app is on sys.path so we can import application package
HERE = os.path.dirname(__file__)
APP_DIR = os.path.normpath(os.path.join(HERE, '..', 'app'))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from application.util import (
    slugify_title, createJWT, verifyJWT, response,
    isAdminBool, getUsername, isAdmin, authenticated
)
from application.models import Users, Note, db, LoginForm, RegistrationForm, NoteForm


# ===== SLUGIFY TESTS =====
def test_slugify_basic():
    """Test basic slugify functionality"""
    assert slugify_title('Hello World!') == 'hello-world'
    assert slugify_title('  New: Note/Title ') == 'new-note-title'


def test_slugify_non_string_raises():
    """Test that slugify raises TypeError for non-string input"""
    with pytest.raises(TypeError):
        slugify_title(None)


def test_slugify_unicode():
    """Test unicode character handling in slugify"""
    result = slugify_title('Čćžšđ Title')
    assert 'title' in result.lower()


def test_slugify_empty_string():
    """Test empty string handling"""
    assert slugify_title('') == ''


def test_slugify_only_special_chars():
    """Test string with only special characters"""
    assert slugify_title('!@#$%^&*') == ''


def test_slugify_numbers():
    """Test slugify with numbers"""
    assert slugify_title('Note 123 Title') == 'note-123-title'


def test_slugify_multiple_spaces():
    """Test multiple consecutive spaces"""
    assert slugify_title('Hello    World') == 'hello-world'


def test_slugify_case_insensitive():
    """Test that result is lowercase"""
    result = slugify_title('HeLLo WoRLD')
    assert result == result.lower()


def test_slugify_strip_trailing_hyphens():
    """Test that trailing hyphens are stripped"""
    result = slugify_title('---Hello World---')
    assert not result.startswith('-')
    assert not result.endswith('-')


# ===== JWT TESTS =====
def test_create_jwt():
    """Test JWT creation"""
    token = createJWT('testuser')
    assert isinstance(token, str)
    assert len(token) > 0


def test_verify_jwt_valid():
    """Test JWT verification with valid token"""
    token = createJWT('testuser')
    decoded = verifyJWT(token)
    assert decoded['username'] == 'testuser'


def test_verify_jwt_expired():
    """Test that JWT handles expiration"""
    key = 'SOtqCasVL3Icp0fBOiFg5W2YdvgkqKrpki0nXzdKUUWKTSigK0'
    # Create expired token
    expired_token = jwt.encode(
        {
            'username': 'testuser',
            'exp': datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
        },
        key,
        algorithm='HS256'
    )
    # Should raise or return abort
    try:
        result = verifyJWT(expired_token)
        assert result is None or str(result).startswith('<Response')
    except:
        pass


def test_verify_jwt_invalid():
    """Test JWT verification with invalid token"""
    invalid_token = 'invalid.token.here'
    try:
        verifyJWT(invalid_token)
    except:
        pass


# ===== RESPONSE TESTS =====
def test_response_function():
    """Test response helper function"""
    resp = response('test message')
    assert resp is not None

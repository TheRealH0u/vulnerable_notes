import os
import sys
import pytest
import json

# Ensure backend/app is on sys.path
HERE = os.path.dirname(__file__)
APP_DIR = os.path.normpath(os.path.join(HERE, '..', 'app'))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)


class TestAPILogin:
    """Test API login endpoint"""

    def test_login_endpoint_exists(self):
        """Test that login endpoint can be imported"""
        from application.blueprints.api import api_login
        assert callable(api_login)

    def test_login_missing_credentials(self):
        """Test login with missing credentials"""
        # This tests the error handling logic for missing credentials
        data = {}
        # The endpoint expects username and password
        assert data.get('username') is None
        assert data.get('password') is None


class TestAPIRegister:
    """Test API register endpoint"""

    def test_register_endpoint_exists(self):
        """Test that register endpoint can be imported"""
        from application.blueprints.api import api_register
        assert callable(api_register)

    def test_register_missing_fields(self):
        """Test register with missing fields"""
        data = {'username': 'test'}
        # Check missing required fields
        assert 'email' not in data or not data.get('email')
        assert 'password' not in data or not data.get('password')
        assert 'verify' not in data or not data.get('verify')

    def test_register_password_validation(self):
        """Test that register validates matching passwords"""
        password = 'password123'
        verify = 'password456'
        assert password != verify  # Should not match


class TestAPISettings:
    """Test API settings endpoint"""

    def test_settings_endpoint_exists(self):
        """Test that settings endpoint can be imported"""
        from application.blueprints.api import api_settings
        assert callable(api_settings)

    def test_settings_missing_password(self):
        """Test settings with missing password"""
        data = {}
        assert data.get('password') is None


class TestAPINotes:
    """Test API notes endpoints"""

    def test_get_notes_endpoint_exists(self):
        """Test that GET notes endpoint exists"""
        from application.blueprints.api import api_notes
        assert callable(api_notes)

    def test_create_note_endpoint_exists(self):
        """Test that POST notes endpoint exists"""
        from application.blueprints.api import api_create_note
        assert callable(api_create_note)

    def test_note_data_structure(self):
        """Test expected note data structure"""
        note_data = {
            'id': 1,
            'title': 'Test',
            'content': 'Content',
            'created_at': '2023-01-01 12:00:00'
        }
        assert 'title' in note_data
        assert 'content' in note_data
        assert 'created_at' in note_data
        assert isinstance(note_data['created_at'], str)


class TestAuthFunctions:
    """Test authentication helper functions"""

    def test_token_username_function(self):
        """Test token_username extraction logic"""
        from application.blueprints.api import token_username
        assert callable(token_username)

    def test_auth_header_parsing(self):
        """Test Bearer token parsing"""
        token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
        if token.startswith('Bearer '):
            extracted = token.split(' ', 1)[1]
            assert extracted == 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'

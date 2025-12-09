import os
import sys
import pytest

# Ensure backend/app is on sys.path
HERE = os.path.dirname(__file__)
APP_DIR = os.path.normpath(os.path.join(HERE, '..', 'app'))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from application.models import Users, Note, LoginForm, RegistrationForm, NoteForm


class TestUsersModel:
    """Test Users model"""

    def test_users_repr(self):
        """Test Users __repr__ method"""
        user = Users(id=1, username='testuser', email='test@test.com', password='hash')
        assert 'testuser' in repr(user)
        assert 'test@test.com' in repr(user)

    def test_users_attributes(self):
        """Test Users model has required attributes"""
        user = Users(username='john', email='john@example.com', password='hashed')
        assert user.username == 'john'
        assert user.email == 'john@example.com'
        assert user.password == 'hashed'


class TestNoteModel:
    """Test Note model"""

    def test_note_repr(self):
        """Test Note __repr__ method"""
        note = Note(id=1, user_id=1, title='Test Note', content='Content')
        assert 'Test Note' in repr(note)
        assert 'user_id' in repr(note).lower() or '1' in repr(note)

    def test_note_attributes(self):
        """Test Note model has required attributes"""
        note = Note(title='My Note', content='Note content', user_id=1)
        assert note.title == 'My Note'
        assert note.content == 'Note content'
        assert note.user_id == 1


class TestLoginForm:
    """Test LoginForm validation"""

    def test_login_form_exists(self):
        """Test LoginForm class exists"""
        assert LoginForm is not None

    def test_login_form_has_fields(self):
        """Test LoginForm has required fields defined"""
        # Check that form class has the field definitions
        assert hasattr(LoginForm, 'username')
        assert hasattr(LoginForm, 'password')
        assert hasattr(LoginForm, 'submit')


class TestRegistrationForm:
    """Test RegistrationForm validation"""

    def test_registration_form_exists(self):
        """Test RegistrationForm class exists"""
        assert RegistrationForm is not None

    def test_registration_form_has_fields(self):
        """Test RegistrationForm has required fields defined"""
        # Check that form class has the field definitions
        assert hasattr(RegistrationForm, 'username')
        assert hasattr(RegistrationForm, 'email')
        assert hasattr(RegistrationForm, 'password')
        assert hasattr(RegistrationForm, 'verify')
        assert hasattr(RegistrationForm, 'submit')


class TestNoteForm:
    """Test NoteForm validation"""

    def test_note_form_exists(self):
        """Test NoteForm class exists"""
        assert NoteForm is not None

    def test_note_form_has_fields(self):
        """Test NoteForm has required fields defined"""
        # Check that form class has the field definitions
        assert hasattr(NoteForm, 'title')
        assert hasattr(NoteForm, 'content')
        assert hasattr(NoteForm, 'submit')

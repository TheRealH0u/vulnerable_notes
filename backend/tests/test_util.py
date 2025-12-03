import os
import sys
import pytest

# Ensure backend/app is on sys.path so we can import application package
HERE = os.path.dirname(__file__)
APP_DIR = os.path.normpath(os.path.join(HERE, '..', 'app'))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from application.util import slugify_title


def test_slugify_basic():
    assert slugify_title('Hello World!') == 'hello-world'
    assert slugify_title('  New: Note/Title ') == 'new-note-title'


def test_slugify_non_string_raises():
    with pytest.raises(TypeError):
        slugify_title(None)


def test_slugify_unicode():
    # Unicode characters should be normalized/removed where possible
    assert slugify_title('Čćžšđ Title') == 'cczsd-title' or slugify_title('Čćžšđ Title') == 'cczsd-title'

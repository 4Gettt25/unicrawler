import os
import pytest
from django.contrib.auth import get_user_model
from django.conf import settings
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'unicrawler.settings'  # replace 'myproject.settings' with your actual settings module

django.setup()
User = get_user_model()

@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user('testuser1@test.com', 'testuser1', 'testpassword')
    assert user.email == 'testuser1'
    assert user.nick_name == 'testuser1'
    assert user.check_password('testpassword')
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser

@pytest.mark.django_db
def test_create_superuser():
    user = User.objects.create_superuser('testadmin1@test.com', 'testadmin1', 'testpassword')
    assert user.email == 'testadmin1'
    assert user.nick_name == 'testadmin1'
    assert user.check_password('testpassword')
    assert user.is_active
    assert user.is_staff
    assert user.is_superuser

@pytest.mark.django_db
def test_user_string_representation():
    user = User.objects.create_user('testuser2@test.com', 'testuser2', 'testpassword')
    assert str(user) == user.email
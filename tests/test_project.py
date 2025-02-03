import pytest
import random
import string
from unittest.mock import patch
from src.project import Password_manager

@pytest.fixture
def manager():
    return Password_manager()

#tests encryption and decryption with a mock key
def test_encryption_decryption(manager):
    original_data = {"newsite.com": {"username": "testuser", "password": "testpassword"}}

    encrypted_data = manager.encrypt_file(original_data)

    decrypted_data = manager.decrypt_file(encrypted_data)

    assert decrypted_data == original_data, "Decryption has failed. Original data does not match decrypted data."

#tests to ensure encrypted data does not match original data 
def test_encryption_is_different(manager):
    original_data = {"newsite.com": {"username": "testuser", "password": "testpassword"}}

    encrypted_data = manager.encrypt_file(original_data)

    assert encrypted_data != original_data, "Encryption failed! Encrypted data matches original data when it should not."

#tests add class function 
def test_add_password(manager):
    #set up for test case
    app_website = "newsite.com"
    username = "testuser"
    password = "testpassword"

    manager.add(app_website, username, password)

    assert app_website in manager.password_dict
    assert manager.password_dict[app_website]["username"] == username
    assert manager.password_dict[app_website]["password"] == password

#tests update class function
def test_update_password(manager):
    #set up for test case
    app_website = "newsite.com"
    username = "testuser"
    old_password = "oldpassword"
    manager.add(app_website, username, old_password)

    # mocks user input for old and new passwords
    with patch('builtins.input', side_effect=['oldpassword', 'newpassword']):
        
        manager.update(app_website)

        assert manager.password_dict[app_website]["password"] == 'newpassword'

#tests delete class function
def test_delete_password(manager):
    #set up for test case
    app_website = "newsite.com"
    username = "testuser"
    password = "testpassword"
    manager.add(app_website, username, password)

    # mocks user input for old password
    with patch('builtins.input', side_effect=['testpassword']):

        manager.delete(app_website)

        assert app_website not in manager.password_dict
"""Utility functions for the MySQL Schema Diff Reporter."""
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json
import streamlit as st

# Use a constant salt for our simple encryption
SALT = b'mysql_schema_diff_salt'

def get_key():
    """Generate a key for encryption using a constant salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(b'mysql_schema_diff_key'))
    return key

def encrypt_value(value: str) -> str:
    """Encrypt a string value."""
    if not value:
        return ""
    f = Fernet(get_key())
    return f.encrypt(value.encode()).decode()

def decrypt_value(encrypted_value: str) -> str:
    """Decrypt an encrypted string value."""
    if not encrypted_value:
        return ""
    f = Fernet(get_key())
    return f.decrypt(encrypted_value.encode()).decode()

def save_connection_details(host: str, port: int, username: str, password: str, old_db: str, new_db: str):
    """Save connection details to local storage."""
    details = {
        'host': host,
        'port': port,
        'username': username,
        'password': encrypt_value(password),
        'old_db': old_db,
        'new_db': new_db
    }
    st.session_state['connection_details'] = details
    # Use streamlit's experimental local storage API
    st.session_state['saved_connection'] = True

def load_connection_details():
    """Load connection details from local storage."""
    if 'connection_details' not in st.session_state:
        return None
    
    details = st.session_state['connection_details']
    if details and 'password' in details:
        # Decrypt the password
        details['password'] = decrypt_value(details['password'])
    return details

def clear_connection_details():
    """Clear saved connection details."""
    if 'connection_details' in st.session_state:
        del st.session_state['connection_details']
    if 'saved_connection' in st.session_state:
        del st.session_state['saved_connection']

"""Utility functions for the MySQL Schema Diff Reporter."""
import base64
import json
import streamlit as st

# Simple encryption key
KEY = b'mysql_schema_diff_key_123'

def xor_encrypt(data: bytes, key: bytes) -> bytes:
    """Simple XOR encryption."""
    return bytes(a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1)))

def encrypt_value(value: str) -> str:
    """Encrypt a string value."""
    if not value:
        return ""
    data = value.encode()
    encrypted = xor_encrypt(data, KEY)
    return base64.urlsafe_b64encode(encrypted).decode()

def decrypt_value(encrypted_value: str) -> str:
    """Decrypt an encrypted string value."""
    if not encrypted_value:
        return ""
    try:
        encrypted = base64.urlsafe_b64decode(encrypted_value.encode())
        decrypted = xor_encrypt(encrypted, KEY)  # XOR is its own inverse
        return decrypted.decode()
    except:
        return ""

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

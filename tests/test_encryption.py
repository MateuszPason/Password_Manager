import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.encryption import derive_key_pbkdf2_sha256, encrypt_password, decrypt_password

key = derive_key_pbkdf2_sha256("test_master_password")

blob = encrypt_password("testPassword", key)
print("Encrypted length:", len(blob))
print("Decrypted:", decrypt_password(blob, key))


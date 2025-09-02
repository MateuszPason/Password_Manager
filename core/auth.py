import base64
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from core.database import insert_setting, get_setting

ITERATIONS = 200_000

def set_master_password(password: str):
    salt = os.urandom(16)
    hash_val = _derive_key(password, salt)
    insert_setting("master_salt", base64.b64encode(salt).decode())
    insert_setting("master_hash", base64.b64encode(hash_val).decode())

def verify_master_password(password: str) -> bool:
    salt_b64 = get_setting("master_salt")
    hash_b64 = get_setting("master_hash")
    if not salt_b64 or not hash_b64:
        return False
    salt = base64.b64decode(salt_b64)
    stored_hash = base64.b64decode(hash_b64)
    derived_hash = _derive_key(password, salt)
    return derived_hash == stored_hash

def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    return kdf.derive(password.encode())
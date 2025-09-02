import base64
from core.database import get_setting
from core.encryption import derive_key_pbkdf2_sha256

def derive_master_key(master_password: str) -> bytes:
    salt_b64 = get_setting("master_salt")
    if not salt_b64:
        raise ValueError("Master salt not found in DB.")
    salt = base64.b64decode(salt_b64)
    return derive_key_pbkdf2_sha256(master_password + base64.b64encode(salt).decode())
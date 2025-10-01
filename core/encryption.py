import os 
import hashlib
from typing import Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCM # type: ignore
from core.config import SALT_FILE, KDF_ITERATIONS, KEY_LEN, AAD

def _ensure_data_dir() -> None:
    os.makedirs("data", exist_ok=True)

def _generate_salt(n: int = 16) -> bytes:
    return os.urandom(n)

def get_or_create_salt(path:str = SALT_FILE) -> bytes:
    _ensure_data_dir()
    if not os.path.exists(path):
        salt = _generate_salt(16)
        with open(path, "wb") as f:
            f.write(salt)
        return salt
    with open(path, "rb") as f:
        return f.read()
    

def derive_key_pbkdf2_sha256(
        master_password: str,
        salt: Optional[bytes] = None,
        iterations: int = KDF_ITERATIONS,
        key_len: int = KEY_LEN,
) -> bytes:
    if salt is None:
        salt = get_or_create_salt()
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=master_password.encode("utf-8"),
        salt=salt,
        iterations=iterations,
        dklen=key_len,
    )

def encrypt_password(plain_password: str, key: bytes) -> str:
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plain_password.encode("utf-8"), AAD)
    return nonce + ct

def decrypt_password(encrypted: bytes, key: bytes) -> str:
    aesgcm = AESGCM(key)
    nonce, ct = encrypted[:12], encrypted[12:]
    pt = aesgcm.decrypt(nonce, ct, AAD)
    return pt.decode("utf-8")
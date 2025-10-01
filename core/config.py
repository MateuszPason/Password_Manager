import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DB_PATH = os.path.join(DATA_DIR, "vault.db")
SALT_FILE = os.path.join(DATA_DIR, "salt.bin")

KDF_ITERATIONS = 200_000
KEY_LEN = 32
AAD = b"pmgr_v1"

DEFAULT_PASSWORD_LENGTH = 16
PASSWORD_CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{};:,.<>?/"
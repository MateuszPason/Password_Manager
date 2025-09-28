import secrets
from core.database import insert_credential, search_credentials, delete_credential
from core.encryption import encrypt_password, decrypt_password
from core.utils import derive_master_key
from core.models import Credential
import string

class CredentialController:
    def __init__(self, master_password):
        self.master_password = master_password

    def add_credential(self, site: str, username: str, password: str) -> None:
        key = derive_master_key(self.master_password)
        encrypted = encrypt_password(password, key)
        insert_credential(site, username, encrypted)

    def search(self, query: str) -> list[Credential]:
        return search_credentials(query)
    
    def delete(self, cred_id: int) -> None:
        delete_credential(cred_id)
    
    def get_password(self, cred_id: int) -> str | None:
        key = derive_master_key(self.master_password)
        result = search_credentials("", cred_id)
        if result:
            return decrypt_password(result[0].password, key)
        return None
    
    def generate_password(self, length=16) -> str:
        chars = string.ascii_letters + string.digits + string.punctuation
        password = "".join(secrets.choice(chars) for _ in range(length))
        return password
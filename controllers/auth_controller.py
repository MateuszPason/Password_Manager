from core.auth import set_master_password, verify_master_password

class AuthController:
    def __init__(self):
        pass

    def create_master_password(self, password: str) -> None:
        set_master_password(password)

    def check_master_password(self, password: str) -> bool:
        return verify_master_password(password)
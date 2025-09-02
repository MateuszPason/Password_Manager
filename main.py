# main.py
from ui.app_gui import PasswordManagerApp
from core.encryption import derive_key_pbkdf2_sha256
from core.database import initialize_database
from ui.login_gui import LoginWindow

def main():
    initialize_database()
    
    login_window = LoginWindow()
    master_password = login_window.run()

    if not master_password:
        print("Login cancelled!")
        return

    # Launch the main app window
    app = PasswordManagerApp(master_password)
    app.run()

if __name__ == "__main__":
    main()

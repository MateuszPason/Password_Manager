# main.py
from ui.app_gui import PasswordManagerApp
from core.database import initialize_database
from ui.login_gui import LoginWindow

def main():
    initialize_database()
    
    login_window = LoginWindow()
    master_password = login_window.run()

    if master_password:
        # Launch the main app window
        app = PasswordManagerApp(master_password)
        app.run()

if __name__ == "__main__":
    main()

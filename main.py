# main.py
from ui.app_gui import PasswordManagerApp
from core.database import initialize_database
from ui.login_gui import LoginWindow
from controllers.credential_controller import CredentialController
from controllers.ui_controller import UIController

def main():
    initialize_database()
    
    login_window = LoginWindow()
    master_password = login_window.run()

    if master_password:
        # Launch the main app window
        credential_controller = CredentialController(master_password)
        ui_controller = UIController(credential_controller)
        app = PasswordManagerApp(master_password, credential_controller, ui_controller)
        app.run()

if __name__ == "__main__":
    main()

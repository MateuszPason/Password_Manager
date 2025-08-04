from ui.app_gui import PasswordManagerApp
from core.database import initialize_database

def main():
    initialize_database()
    app = PasswordManagerApp()
    app.run()

if __name__ == "__main__":
    main()
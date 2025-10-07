# Password Manager

A secure, modern, and user-friendly password manager built with Python and Tkinter. This application helps you safely store, search, and manage your credentials using strong encryption and a master password.

## Features

- **Master Password Protection**: All credentials are encrypted using a master password that only you know.
- **Strong Encryption**: Uses PBKDF2-HMAC-SHA256 for key derivation and AES-GCM for encrypting passwords.
- **Credential Management**: Add, search, and delete credentials (site, username, password).
- **Password Generator**: Generate strong, random passwords with customizable length.
- **Clipboard Copy**: Securely copy passwords to your clipboard.
- **Password Visibility Toggle**: Show/hide passwords in the UI.
- **User-Friendly Interface**: Simple and intuitive GUI built with Tkinter.
- **First-Run Setup**: Prompts you to create a master password on first launch.
- **Cross-Platform**: Runs on Windows, macOS, and Linux.

## Getting Started

### Prerequisites

- Python 3.10 or newer
- [pip](https://pip.pypa.io/en/stable/)

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/MateuszPason/password-manager.git
   cd password-manager
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```sh
   python main.py
   ```

## Usage

- On first launch, you will be prompted to create a master password.
- Use the "Add Credential" tab to store new credentials.
- Use the "Search Credential" tab to find, view, copy, or delete credentials.
- Use the "Generate Password" button to create strong passwords.

## Security Notes

- All credentials are encrypted using a key derived from your master password and a unique salt.
- The master password is never stored; only a salted hash is saved for verification.
- **Do not forget your master password!** There is no way to recover your credentials without it.

## Project Structure

```
.
├── main.py
├── README.md
├── requirements.txt
├── controllers/
│   ├── auth_controller.py
│   ├── credential_controller.py
│   └── ui_controller.py
├── core/
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── encryption.py
│   ├── models.py
│   └── utils.py
├── data/
│   ├── salt.bin
│   └── vault.db
├── tests/
│   ├── test_auth.py
│   └── test_encryption.py
└── ui/
    ├── app_gui.py
    └── login_gui.py
```

## License

This project is licensed under the MIT License.

## Acknowledgements

- [cryptography](https://cryptography.io/) for secure encryption primitives
- Python's [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI

---

**Disclaimer:** This project is for educational purposes.
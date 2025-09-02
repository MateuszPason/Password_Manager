import tkinter as tk
from tkinter import ttk, messagebox
from core.database import get_setting, insert_setting
from core.encryption import derive_key_pbkdf2_sha256
import base64
import os

ITERATIONS = 200_000

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Manager - Login")
        self.root.geometry("450x280")
        self.master_password = None
        self.is_first_run = get_setting("master_hash") is None

        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        if self.is_first_run:
            ttk.Label(frame, text="Create Master Password:").pack(pady=10)
            ttk.Label(frame, text="Confirm Master Password:").pack(pady=5)
            self.password_entry = ttk.Entry(frame, show="*", width=25)
            self.password_entry.pack(pady=5)
            self.confirm_entry = ttk.Entry(frame, show="*", width=25)
            self.confirm_entry.pack(pady=5)
        else:
            ttk.Label(frame, text="Enter Master Password:").pack(pady=10)
            self.password_entry = ttk.Entry(frame, show="*", width=25)
            self.password_entry.pack(pady=10)

        ttk.Button(frame, text="Submit", command=self._on_submit).pack(pady=10)

    def _on_submit(self):
        pwd = self.password_entry.get().strip()
        if self.is_first_run:
            confirm = self.confirm_entry.get().strip()
            if not pwd or not confirm:
                messagebox.showerror("Error", "Please fill both fields.")
                return
            if pwd != confirm:
                messagebox.showerror("Error", "Passwords do not match.")
                return
            self._set_master_password(pwd)
        else:
            if not pwd:
                messagebox.showerror("Error", "Master password cannot be empty.")
                return
            if not self._verify_master_password(pwd):
                messagebox.showerror("Error", "Incorrect master password.")
                return
        self.master_password = pwd
        self.root.destroy()

    def _set_master_password(self, password: str):
        salt = os.urandom(16)
        key = derive_key_pbkdf2_sha256(password + base64.b64encode(salt).decode())
        insert_setting("master_salt", base64.b64encode(salt).decode())
        insert_setting("master_hash", base64.b64encode(key).decode())
        messagebox.showinfo("Success", "Master password created!")

    def _verify_master_password(self, password: str) -> bool:
        salt_b64 = get_setting("master_salt")
        hash_b64 = get_setting("master_hash")
        if not salt_b64 or not hash_b64:
            return False
        salt = base64.b64decode(salt_b64)
        stored_key = base64.b64decode(hash_b64)
        entered_key = derive_key_pbkdf2_sha256(password + base64.b64encode(salt).decode())
        return entered_key == stored_key


    def run(self):
        self.root.mainloop()
        return self.master_password
             
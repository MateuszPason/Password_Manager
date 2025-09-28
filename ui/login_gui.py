import tkinter as tk
from tkinter import ttk, messagebox
from core.database import get_setting
from controllers.auth_controller import AuthController

ITERATIONS = 200_000

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Manager - Login")
        self.root.geometry("450x280")
        self.master_password = None
        self.auth_controller = AuthController()
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
            self.auth_controller.create_master_password(pwd)
        else:
            if not pwd:
                messagebox.showerror("Error", "Master password cannot be empty.")
                return
            if not self.auth_controller.check_master_password(pwd):
                messagebox.showerror("Error", "Incorrect master password.")
                return
        self.master_password = pwd
        self.root.destroy()

    def run(self):
        self.root.mainloop()
        return self.master_password
             
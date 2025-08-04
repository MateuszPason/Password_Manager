import tkinter as tk
import tkinter.messagebox as messagebox

class PasswordManagerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Manager")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.current_frame = None
        self._show_login_screen()

    def _clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def _show_login_screen(self):
        self._clear_frame()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)

        tk.Label(self.current_frame, text="Enter Master Password", font=("Arial", 14))

        self.master_password_entry = tk.Entry(self.current_frame, show='*', width=30)
        self.master_password_entry.pack(pady=10)

        tk.Button(self.current_frame, text="Unlock", command=self._on_unlock).pack(pady=10)

    def _on_unlock(self):
        password = self.master_password_entry.get()
        if password.strip():
            self._show_main_screen()
        else:
            messagebox.showerror("Error", "Master password is required")

    def _show_main_screen(self):
        self._clear_frame()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)

        tk.Label(self.current_frame, text="Welcome to Password Manager", font=("Arial", 10)).pack(pady=20)

        tk.Button(self.current_frame, text="Exit", command=self.root.quit).pack(pady=10)

    def run(self):
        self.root.mainloop()
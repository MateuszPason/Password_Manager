import tkinter as tk

class PasswordManagerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Manager")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.build_ui()

    def build_ui(self):
        title_label = tk.Label(self.root, text="Password Manager", font=("Arial", 16))
        title_label.pack(pady=20)

        exit_button = tk.Button(self.root, text='Exit', command=self.root.quit)
        exit_button.pack(pady=10)

    def run(self):
        self.root.mainloop()
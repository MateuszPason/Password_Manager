import tkinter as tk
from tkinter import ttk, messagebox
from core.database import insert_credential, search_credentials, delete_credential
from core.encryption import encrypt_password, decrypt_password
from core.utils import derive_master_key
import string
import secrets

class PasswordManagerApp:
    def __init__(self, master_password):
        self.master_password = master_password
        self.root = tk.Tk()
        self.root.title("Password Manager")
        self.root.geometry("700x500")
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)
        self.notebook.pack(expand=True, fill="both")

        self.add_tab = ttk.Frame(self.notebook)
        self.search_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.add_tab, text="Add Credential")
        self.notebook.add(self.search_tab, text="Search Credential")

        self._build_add_tab()
        self._build_search_tab()

    def _on_tab_change(self, event):
        selected_tab = event.widget.tab(event.widget.index("current"))["text"]
        if selected_tab == "Search Credential":
            self.search_entry.delete(0, tk.END)
            self._load_all_credentials()

    def _load_all_credentials(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        results = search_credentials("")

        for r in results:
            self.tree.insert("", tk.END, values=(r[1], r[2]), iid=r[0])

    def _build_add_tab(self):
        # Create a frame to center the form
        form_frame = ttk.Frame(self.add_tab)
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Configure grid for responsiveness
        for i in range(3):
            form_frame.rowconfigure(i, weight=1)
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=2)
        form_frame.columnconfigure(2, weight=0)

        tk.Label(form_frame, text="Site:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        tk.Label(form_frame, text="Username:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        tk.Label(form_frame, text="Password:").grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.site_entry = tk.Entry(form_frame)
        self.username_entry = tk.Entry(form_frame)
        self.password_entry = tk.Entry(form_frame, show="*")

        self.site_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.username_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.password_entry.grid(row=2, column=1, padx=(10, 0), pady=10, sticky="ew")
        self.show_password_btn = tk.Button(form_frame, text="Show", width=6, command=self._toggle_password_visibility)
        self.show_password_btn.grid(row=2, column=2, padx=(5, 10), pady=10, sticky="ew")

        tk.Button(form_frame, text="Add", command=self._add_credential).grid(row=3, column=0, padx=10, pady=20, sticky="ew")
        tk.Button(form_frame, text="Generate Password", command=self._generate_password).grid(row=3, column=1, padx=10, pady=20, sticky="ew")

    def _build_search_tab(self):
        tk.Label(self.search_tab, text="Search by Site/Username:").pack(pady=10)
        self.search_entry = tk.Entry(self.search_tab, width=40)
        self.search_entry.pack(pady=5)

        tk.Button(self.search_tab, text="Search", command=self._search_vault).pack(pady=5)

        self.tree = ttk.Treeview(self.search_tab, columns=("site", "username"), show="headings")
        self.tree.heading("site", text="Site")  
        self.tree.heading("username", text="Username")
        self.tree.pack(expand=True, fill="both", pady=10)

        button_frame = tk.Frame(self.search_tab)
        button_frame.pack(pady=10)

        self.context_menu = tk.Menu(self.search_tab, tearoff=0)
        self.context_menu.add_command(label="Show Password", command=self._show_password)
        self.context_menu.add_command(label="Delete Credential", command=self._delete_credential)
        self.context_menu.add_command(label="Copy to Clipboard", command=self._copy_to_clipboard)

        self.tree.bind("<Button-2>", self._show_context_menu)
        self.tree.bind("<Button-3>", self._show_context_menu)
        self.tree.bind("<Control-Button-1>", self._show_context_menu)


    def _add_credential(self):
        site = self.site_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not site or not username or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            key = derive_master_key(self.master_password)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        
        encrypted = encrypt_password(password, key)
        insert_credential(site, username, encrypted)

        messagebox.showinfo("Success", f"Credential for {site} added!")
        self.site_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def _search_vault(self):
        query = self.search_entry.get().strip()
        results = search_credentials(query)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for r in results:
            self.tree.insert("", tk.END, values=(r[1], r[2]), iid=r[0])

    def _show_password(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a credential first!")
            return
        
        cred_id = selected[0]
        results = search_credentials("", cred_id)
        if not results:
            messagebox.showerror("Error", "Credential not found!")
            return
        
        encrypted_pass = results[0][3]

        try:
            key = derive_master_key(self.master_password)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        try:
            decrypted_pass = decrypt_password(encrypted_pass, key)
            messagebox.showinfo("Password", f"Password: {decrypted_pass}")
        except Exception:
            messagebox.showerror("Error", "Failed to decrypt password. It may be corrupted or the key is invalid.")

    def _delete_credential(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a credential first!")
            return
        
        cred_id = selected[0]
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this credential?")
        if not confirm:
            return
        
        try:
            delete_credential(cred_id)
            self.tree.delete(cred_id)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete credential: {str(e)}")

    def _copy_to_clipboard(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a credential first!")
            return
        
        cred_id = selected[0]
        results = search_credentials("", cred_id)
        if not results:
            messagebox.showerror("Error", "Credential not found!")
            return
        
        encrypted_pass = results[0][3]

        try:
            key = derive_master_key(self.master_password)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        try:
            decrypted_pass = decrypt_password(encrypted_pass, key)
            self.root.clipboard_clear()
            self.root.clipboard_append(decrypted_pass)
            self.root.update()
            messagebox.showinfo("Success", "Password copied to clipboard!")
        except Exception:
            messagebox.showerror("Error", "Failed to decrypt password. It may be corrupted or the key is invalid.")

    def _generate_password(self, length=16):
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(chars) for _ in range(length))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def _toggle_password_visibility(self):
        if self.password_entry.cget("show") == "*":
            self.password_entry.config(show='')
            self.show_password_btn.config(text="Hide")
        else:
            self.password_entry.config(show="*")
            self.show_password_btn.config(text="Show")

    def _show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def run(self):
        self.root.mainloop()

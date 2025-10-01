import tkinter as tk
from tkinter import ttk, messagebox

class PasswordManagerApp:
    def __init__(self, master_password, credential_controller, ui_controller):
        self.credential_controller = credential_controller
        self.ui_controller = ui_controller
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
        self.show_password_btn = tk.Button(form_frame, text="Show", width=6, command=self._on_toggle_password_visibility_clicked)
        self.show_password_btn.grid(row=2, column=2, padx=(5, 10), pady=10, sticky="ew")

        tk.Button(form_frame, text="Add", command=self._on_add_clicked).grid(row=3, column=0, padx=10, pady=20, sticky="ew")
        tk.Button(form_frame, text="Generate Password", command=self._on_generate_password_clicked).grid(row=3, column=1, padx=10, pady=20, sticky="ew")

    def _build_search_tab(self):
        tk.Label(self.search_tab, text="Search by Site/Username:").pack(pady=10)
        self.search_entry = tk.Entry(self.search_tab, width=40)
        self.search_entry.pack(pady=5)

        tk.Button(self.search_tab, text="Search", command=self._on_search_clicked).pack(pady=5)

        self.tree = ttk.Treeview(self.search_tab, columns=("site", "username"), show="headings")
        self.tree.heading("site", text="Site")  
        self.tree.heading("username", text="Username")
        self.tree.pack(expand=True, fill="both", pady=10)

        button_frame = tk.Frame(self.search_tab)
        button_frame.pack(pady=10)

        self.context_menu = tk.Menu(self.search_tab, tearoff=0)
        self.context_menu.add_command(label="Show Password", command=self._on_show_password_clicked)
        self.context_menu.add_command(label="Delete Credential", command=self._on_delete_credential_clicked)
        self.context_menu.add_command(label="Copy to Clipboard", command=self._on_copy_to_clipboard_clicked)

        self.tree.bind("<Button-2>", self._on_show_context_menu)
        self.tree.bind("<Button-3>", self._on_show_context_menu)
        self.tree.bind("<Control-Button-1>", self._on_show_context_menu)

    def _on_tab_change(self, event):
        selected_tab = event.widget.tab(event.widget.index("current"))["text"]
        if selected_tab == "Search Credential":
            self.search_entry.delete(0, tk.END)
            self._load_all_credentials()

    def _load_all_credentials(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        results = self.credential_controller.search("")
        for cred in results:
            self.tree.insert("", tk.END, values=(cred.site, cred.username), iid=cred.id)

    def _on_add_clicked(self):
        site = self.site_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        success, msg = self.ui_controller.add_credential(site, username, password)
        if success:
            self.site_entry.delete(0, "end")
            self.username_entry.delete(0, "end")
            self.password_entry.delete(0, "end")
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

    def _on_search_clicked(self):
        query = self.search_entry.get().strip()
        results = self.ui_controller.search_vault(query)
        self.tree.delete(*self.tree.get_children())
        for cred in results:
            self.tree.insert("", "end", values=(cred.site, cred.username), iid=cred.id)

    def _on_show_password_clicked(self):
        selected = self.tree.selection()
        cred_id = int(selected[0])
        success, result = self.ui_controller.show_password(cred_id)
        if success:
            messagebox.showinfo("Password", f"Password: {result}")
        else:
            messagebox.showerror("Error", result)

    def _on_delete_credential_clicked(self):
        selected = self.tree.selection()
        cred_id = int(selected[0])
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this credential?")
        if not confirm:
            return
        success, msg = self.ui_controller.delete_credential(cred_id)
        if success:
            self.tree.delete(cred_id)
        else:
            messagebox.showerror("Error", msg)
    
    def _on_copy_to_clipboard_clicked(self):
        selected = self.tree.selection()
        cred_id = int(selected[0])
        success, result = self.ui_controller.copy_to_clipboard(cred_id)
        if success:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            self.root.update()
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showerror("Error", result)

    def _on_generate_password_clicked(self):
        password = self.ui_controller.generate_password()
        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)

    def _on_toggle_password_visibility_clicked(self):
        current_show = self.password_entry.cget("show")
        new_show, btn_text = self.ui_controller.toggle_password_visibility(current_show)
        self.password_entry.config(show=new_show)
        self.show_password_btn.config(text=btn_text)

    def _on_show_context_menu(self, event):
        self.ui_controller.show_context_menu(self.tree, self.context_menu, event)

    def run(self):
        self.root.mainloop()

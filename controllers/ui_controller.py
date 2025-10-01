from tkinter import messagebox
from core.config import DEFAULT_PASSWORD_LENGTH

class UIController:
    def __init__(self, credential_controller):
        self.credential_controller = credential_controller

    def add_credential(self, site, username, password):
        if not site or not username or not password:
            messagebox.showerror("Error", "All fields are required")
            return False, "All fields are required"
        try:
            self.credential_controller.add_credential(site, username, password)
            return True, f"Credential for {site} added!"
        except Exception as e:
            return False, f"Failed to add credential: {str(e)}"

    def search_vault(self, query):
        results = self.credential_controller.search(query)
        return results

    def show_password(self, cred_id):
        try:
             decrypted_pass = self.credential_controller.get_password(cred_id)
             if decrypted_pass is None:
                 return False, "Password not found or decryption failes"
             return True, decrypted_pass
        except Exception:
            return False, "Failed to decrypt password. It may be corrupted or the key is invalid."

    def delete_credential(self, cred_id):   
        try:
            self.credential_controller.delete(cred_id)
            return True, "Credential deleted!"
        except Exception as e:
            return False, f"Failed to delete credential: {str(e)}"

    def copy_to_clipboard(self, cred_id):
        try:
            decrypted_pass = self.credential_controller.get_password(cred_id)
            if decrypted_pass is None:
                return False, "Password not found or decryption failed."
            return True, decrypted_pass
        except Exception:
            return False, "Failed to decrypt password. It may be corrupted or the key is invalid."

    def generate_password(self, length=DEFAULT_PASSWORD_LENGTH):
        password = self.credential_controller.generate_password(length)
        return password

    def toggle_password_visibility(self, current_show):
        if current_show == "*":
            return "", "Hide"
        else:
            return "*", "Show"

    def show_context_menu(self, tree, context_menu, event):
        item = tree.identify_row(event.y)
        if item:
            tree.selection_set(item)
            context_menu.post(event.x_root, event.y_root)
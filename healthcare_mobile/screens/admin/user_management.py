from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from services.api_client import APIClient

class UserManagementScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_client = APIClient()
        self.dialog = None
    
    def on_enter(self):
        self.load_users()
    
    def load_users(self):
        response = self.api_client.get('/admin/users')
        
        if 'error' in response:
            self.show_dialog("Error", response['error'])
            return
        
        users = response.get('users', [])
        self.display_users(users)
    
    def display_users(self, users):
        if hasattr(self.ids, 'users_list'):
            self.ids.users_list.clear_widgets()
        
        for user in users:
            item = TwoLineListItem(
                text=user.get('name', 'N/A'),
                secondary_text=f"{user.get('email', 'N/A')} | Role: {user.get('role', 'N/A')}",
                on_release=lambda x, u=user: self.view_user_detail(u)
            )
            self.ids.users_list.add_widget(item)
    
    def view_user_detail(self, user):
        message = f"""
Name: {user.get('name', 'N/A')}
Email: {user.get('email', 'N/A')}
Role: {user.get('role', 'N/A')}
Status: {user.get('status', 'N/A')}
        """
        self.show_dialog("User Details", message.strip())
    
    def show_dialog(self, title, message):
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

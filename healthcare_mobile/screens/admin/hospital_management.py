from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from services.api_client import APIClient


class HospitalManagementScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_client = APIClient()
        self.dialog = None
        self._loaded = False

    def on_enter(self):
        if not self._loaded:
            self.load_hospitals()

    def load_hospitals(self):
        response = self.api_client.get('/hospitals')
        if 'error' in response:
            self.show_info_dialog("Error", response['error'])
            return
        self.display_hospitals(response.get('hospitals', []))
        self._loaded = True

    def display_hospitals(self, hospitals):
        self.ids.hospitals_list.clear_widgets()
        for hospital in hospitals:
            item = TwoLineListItem(
                text=hospital.get('hospital_name', 'N/A'),
                secondary_text=f"Type: {hospital.get('hospital_type', 'N/A')} | ID: {hospital.get('hospital_id', 'N/A')}",
                on_release=lambda x, h=hospital: self.show_detail_dialog(h)
            )
            self.ids.hospitals_list.add_widget(item)

    # ── Detail dialog with Edit button ──────────────────────────────────────

    def show_detail_dialog(self, hospital):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title=hospital.get('hospital_name', 'Hospital'),
            text=(
                f"Type: {hospital.get('hospital_type', 'N/A')}\n"
                f"ID: {hospital.get('hospital_id', 'N/A')}\n"
                f"Created: {str(hospital.get('created_at', 'N/A'))[:10]}"
            ),
            buttons=[
                MDFlatButton(text="CLOSE", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="EDIT", on_release=lambda x: self._open_edit(hospital)),
            ]
        )
        self.dialog.open()

    def _open_edit(self, hospital):
        self.dialog.dismiss()
        self.show_edit_dialog(hospital)

    # ── Add dialog ──────────────────────────────────────────────────────────

    def show_add_dialog(self):
        if self.dialog:
            self.dialog.dismiss()

        content = MDBoxLayout(orientation='vertical', spacing='12dp',
                              size_hint_y=None, height='120dp')
        name_field = MDTextField(hint_text="Hospital Name", mode="rectangle")
        type_field = MDTextField(hint_text="Hospital Type (e.g. General)", mode="rectangle")
        content.add_widget(name_field)
        content.add_widget(type_field)

        self.dialog = MDDialog(
            title="Add Hospital",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="ADD", on_release=lambda x: self._submit_add(
                    name_field.text.strip(), type_field.text.strip()
                )),
            ]
        )
        self.dialog.open()

    def _submit_add(self, name, h_type):
        if not name or not h_type:
            self.show_info_dialog("Error", "Both fields are required.")
            return
        self.dialog.dismiss()
        response = self.api_client.post('/register_hospital', {
            'hospital_name': name,
            'hospital_type': h_type,
        })
        if 'error' in response:
            self.show_info_dialog("Error", response['error'])
        else:
            hid = response.get('HospitalID', 'N/A')
            self.show_info_dialog("Success", f"Hospital added.\nID: {hid}")
            self._loaded = False
            self.load_hospitals()

    # ── Edit dialog ─────────────────────────────────────────────────────────

    def show_edit_dialog(self, hospital):
        if self.dialog:
            self.dialog.dismiss()

        content = MDBoxLayout(orientation='vertical', spacing='12dp',
                              size_hint_y=None, height='120dp')
        name_field = MDTextField(hint_text="Hospital Name", mode="rectangle",
                                 text=hospital.get('hospital_name', ''))
        type_field = MDTextField(hint_text="Hospital Type", mode="rectangle",
                                 text=hospital.get('hospital_type', ''))
        content.add_widget(name_field)
        content.add_widget(type_field)

        self.dialog = MDDialog(
            title="Edit Hospital",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="SAVE", on_release=lambda x: self._submit_edit(
                    hospital.get('hospital_id'), name_field.text.strip(), type_field.text.strip()
                )),
            ]
        )
        self.dialog.open()

    def _submit_edit(self, hospital_id, name, h_type):
        if not name or not h_type:
            self.show_info_dialog("Error", "Both fields are required.")
            return
        self.dialog.dismiss()
        response = self.api_client.put(f'/hospitals/{hospital_id}', {
            'hospital_name': name,
            'hospital_type': h_type,
        })
        if 'error' in response:
            self.show_info_dialog("Error", response['error'])
        else:
            self.show_info_dialog("Success", "Hospital updated successfully.")
            self._loaded = False
            self.load_hospitals()

    # ── Helpers ─────────────────────────────────────────────────────────────

    def show_info_dialog(self, title, message):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title=title,
            text=message,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
        )
        self.dialog.open()

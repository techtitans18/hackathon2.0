from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineListItem, OneLineListItem
from services.api_client import APIClient

class SystemLogsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_client = APIClient()
        self._loaded = False

    def on_enter(self):
        if not self._loaded:
            self.load_logs()

    def load_logs(self):
        # Use blockchain as the audit log — it's the immutable record trail
        response = self.api_client.get('/blockchain')
        logs_list = self.ids.logs_list
        logs_list.clear_widgets()
        if 'error' in response:
            logs_list.add_widget(OneLineListItem(text="Failed to load audit log."))
            return
        chain = response.get('chain', [])
        if not chain:
            logs_list.add_widget(OneLineListItem(text="No audit entries found."))
            return
        for block in reversed(chain):
            ts = str(block.get('Timestamp', block.get('timestamp', 'N/A')))[:19]
            logs_list.add_widget(TwoLineListItem(
                text=f"Block #{block.get('Index', '?')} — {block.get('RecordType', 'N/A')} | {block.get('HealthID', '')}",
                secondary_text=f"{ts} | Hospital: {block.get('HospitalID', 'N/A')}"
            ))
        self._loaded = True

    def go_back(self):
        self.manager.current = 'admin_dashboard'

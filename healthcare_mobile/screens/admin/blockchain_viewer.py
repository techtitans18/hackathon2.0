from kivymd.uix.screen import MDScreen
from services.api_client import APIClient

class BlockchainViewerScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_client = APIClient()
        self._loaded = False

    def on_enter(self):
        if not self._loaded:
            self.load_blocks()

    def load_blocks(self):
        response = self.api_client.get('/blockchain')
        blocks_list = self.ids.blocks_list
        blocks_list.clear_widgets()
        from kivymd.uix.list import TwoLineListItem, OneLineListItem
        if 'error' in response:
            blocks_list.add_widget(OneLineListItem(text="Failed to load blockchain."))
            return
        integrity = response.get('integrity', {}).get('valid', False)
        blocks_list.add_widget(OneLineListItem(
            text=f"Chain Length: {response.get('length', 0)} | Integrity: {'✓ Valid' if integrity else '✗ Invalid'}"
        ))
        for block in response.get('chain', []):
            h = str(block.get('Hash', block.get('hash', '')))[:40]
            blocks_list.add_widget(TwoLineListItem(
                text=f"Block #{block.get('Index', block.get('index', '?'))} — {block.get('RecordType', '')}",
                secondary_text=f"Hash: {h}..."
            ))
        self._loaded = True

    def go_back(self):
        self.manager.current = 'admin_dashboard'

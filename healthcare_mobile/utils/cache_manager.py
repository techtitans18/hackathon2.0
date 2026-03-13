import json
import os
from datetime import datetime, timedelta
from typing import Any, Optional

class CacheManager:
    def __init__(self, cache_dir: str = 'cache'):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_path(self, key: str) -> str:
        return os.path.join(self.cache_dir, f"{key}.json")
    
    def set(self, key: str, data: Any, ttl_hours: int = 24):
        cache_data = {
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'expires': (datetime.now() + timedelta(hours=ttl_hours)).isoformat()
        }
        
        with open(self._get_cache_path(key), 'w') as f:
            json.dump(cache_data, f)
    
    def get(self, key: str) -> Optional[Any]:
        cache_path = self._get_cache_path(key)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r') as f:
                cache_data = json.load(f)
            
            expires = datetime.fromisoformat(cache_data['expires'])
            if datetime.now() > expires:
                self.delete(key)
                return None
            
            return cache_data['data']
        except Exception as e:
            print(f"Cache read error: {e}")
            return None
    
    def delete(self, key: str):
        cache_path = self._get_cache_path(key)
        if os.path.exists(cache_path):
            os.remove(cache_path)
    
    def clear_all(self):
        for file in os.listdir(self.cache_dir):
            os.remove(os.path.join(self.cache_dir, file))

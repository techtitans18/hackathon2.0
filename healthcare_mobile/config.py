import os

# API Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://127.0.0.1:8000')
API_TIMEOUT = 30

# Security
TOKEN_KEY = 'healthcare_token'
REFRESH_TOKEN_KEY = 'healthcare_refresh_token'

# Storage
CACHE_DIR = 'cache'
MAX_CACHE_SIZE_MB = 100

# App Settings
APP_VERSION = '1.0.0'
DEBUG_MODE = True

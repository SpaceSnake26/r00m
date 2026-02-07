import os
from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

class Config:
    WIFI_SSID = os.getenv("WIFI_SSID", "Room5012")
    WIFI_PASSWORD = os.getenv("WIFI_PASSWORD", "mancave5012")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_change_me")
    
    # Anti-Abuse settings
    MAX_ATTEMPTS = 8
    COOLDOWN_SECONDS = 600  # 10 minutes

config = Config()

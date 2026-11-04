import requests
import os
from dotenv import load_dotenv
load_dotenv(".env")
updates = requests.get(f"https://api.telegram.org/bot{os.getenv('9043715463')}/getUpdates")
updates = updates.json()
print(updates["result"][-1])
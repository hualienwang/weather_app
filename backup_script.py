# backup_script.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def trigger_backup():
    api_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    try:
        response = requests.get(f"{api_url}/backup/trigger", timeout=30)
        if response.status_code == 200:
            print("✅ 備份觸發成功")
        else:
            print(f"❌ 備份失敗: {response.text}")
    except Exception as e:
        print(f"💥 備份錯誤: {e}")

if __name__ == "__main__":
    trigger_backup()
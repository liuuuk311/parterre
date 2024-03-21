import requests
from django.conf import settings


URL = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={settings.TELEGRAM_TO_CHAT}&text="

def send_message_to_telegram(msg: str):
    requests.get(URL + msg)
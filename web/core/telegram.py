import requests
from django.conf import settings




def send_message_to_telegram(msg: str):
    response = requests.get(settings.TELEGRAM_URL + msg)
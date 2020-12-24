import os

import time
import requests
import logging
from twilio.rest import Client

from dotenv import load_dotenv 
load_dotenv()

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
number_from = os.getenv('NUMBER_FROM')
number_to = os.getenv('NUMBER_TO')
url = os.getenv('URL')
v = os.getenv('VK_API_VERSION')  
access_token = os.getenv('ACCESS_TOKEN')

client = Client(account_sid, auth_token)


def sms_sender(sms_text):
    message = client.messages \
                .create(
                     body=sms_text,
                     from_=number_from,
                     to=number_to)
    return message.sid


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'fields': 'online',
        'v': v,
        'access_token': access_token
    }
    try:
        user_status = requests.post(url, params=params).json()['response'][0]['online']    
        return user_status
    except requests.exceptions.RequestException as e:
        logging.exception(f'Request raised error: {e}')    



if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)

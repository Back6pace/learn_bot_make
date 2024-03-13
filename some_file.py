import requests
import time

bot_api_url = 'https://api.telegram.org/bot'
bot_token = 'bot_token'

offset = -2
counter = 0
timeout = -5
updates: dict


def do_something() -> None:
    print('Был апдейт')


while True:
    start_time = time.time()
    updates = requests.get(
        f"{bot_api_url}{bot_token}/getUpdates?offset={offset + 1}&timeout={timeout}").json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            do_something()
    end_time = time.time()
    print(
        f"Время между запросами к телеграм бот апи = {end_time - start_time}")

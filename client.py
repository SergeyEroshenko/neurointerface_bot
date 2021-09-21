import os
import sys
import time
import asyncio
import random

from telethon import TelegramClient, events, utils
from security_data import CLIENT_ID, CLIENT_HASH
from settings import BOT_NAME


def get_env(name, message, cast=str):
    if name in os.environ:
        return os.environ[name]
    while True:
        value = input(message)
        try:
            return cast(value)
        except ValueError as e:
            print(e, file=sys.stderr)
            time.sleep(1)


session = os.environ.get('TG_SESSION', 'neurointerface')
api_id = CLIENT_ID # get_env('TG_API_ID', 'Enter your API ID: ', int)
api_hash = CLIENT_HASH # get_env('TG_API_HASH', 'Enter your API hash: ')
proxy = None 
buttons = list(range(4))
client = TelegramClient(session, api_id, api_hash, proxy=proxy).start()


@client.on(events.NewMessage(from_users=BOT_NAME))
async def handler(event):
    await asyncio.sleep(3)
    await event.click(random.choice(buttons))


try:
    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()
finally:
    client.disconnect()
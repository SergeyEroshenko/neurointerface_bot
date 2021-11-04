import os
import asyncio
import random

from telethon import TelegramClient, events
from security_data import CLIENT_ID, CLIENT_HASH
from settings import BOT_NAME


session = os.environ.get('TG_SESSION', 'neurointerface')
api_id = CLIENT_ID
api_hash = CLIENT_HASH
proxy = None 
buttons = list(range(4))
client = TelegramClient(session, api_id, api_hash, proxy=proxy).start()


@client.on(events.NewMessage(from_users=[BOT_NAME, 'me']))
async def handler(event):
    if event.message.message == "/stop":
        await client.disconnect()
    await asyncio.sleep(3)
    await event.click(random.choice(buttons))


try:
    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()
finally:
    client.disconnect()

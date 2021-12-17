# import json
import websockets
from typing import List, Optional
from .observer import Subject, Observer


class BaseConnector(Subject):

    uri: Optional[str] = None

    def __init__(self):
        self.connection = None
        self._observers: List[Observer] = []
        self._state: str = ""

        if self.uri is None:
            raise ValueError(
                "self.uri not defined. Pleas define is as ws://host:port")

    async def connect(self):
        # открываем соединение
        self.connection = await websockets.connect(
            uri=self.uri,
        )

    async def disconnect(self):
        # закрываем соединение
        await self.connection.close()

    async def handler(self):
        # получатель собщений из установленного соединения
        async for message in self.connection:
            self._state = message
            # msg = json.loads(message)
            # print(msg['command'])
            self.notify()

import websockets
from typing import List
from .observer import ConcreteSubject, Observer


class BaseConnector(ConcreteSubject):

    uri: str = None

    def __init__(self):
        self.connection = None
        self._observers: List[Observer] = []
        self._state: str = None

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
            self.notify()

import asyncio
import re
import json
import ciso8601
import websockets
from time import strptime
from typing import List
from ..core import Observer, ConcreteSubject


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

    async def handler(self):
        # получатель собщений из установленного соединения
        async for message in self.connection:
            self._state = message
            self.notify()


class Connector(BaseConnector):
    
    uri: str = "ws://127.0.0.1:1336"

    def __init__(self, device_id: str, freq: int):
        self.device_id = device_id
        self.freq = freq

        self.connection = None
        self._observers: List[Observer] = []
        self._state: str = None

    async def start_search(self):
        msg = json.dumps({"command": "startSearch"})
        await self.connection.send(msg)

    async def stop_search(self):
        msg = json.dumps({"command": "stopSearch"})
        await self.connection.send(msg)

    async def list_devices(self):
        msg = json.dumps({"command": "listDevices"})
        await self.connection.send(msg)

    async def device_count(self):
        msg = json.dumps({"command": "deviceCount"})
        await self.connection.send(msg)

    async def get_device_info(self, sn: str, index: int):
        msg = json.dumps({
            "command": "startDevice",
            "SN": sn,
            "index": index
            })
        await self.connection.send(msg)

    async def start_device(self, sn: str, channels: int, index: int):
        msg = json.dumps({
            "command": "startDevice",
            "SN": sn,
            "channels": channels, 
            "index": index,
            })
        await self.connection.send(msg)

    async def current_device_info(self):
        msg = json.dumps({"command": "currentDeviceInfo"})
        await self.connection.send(msg)

    async def make_favorite(self, value: str):
        msg = json.dumps({
            "command": "makeFavorite",
            "value": value
            })
        await self.connection.send(msg)

    async def get_favorite_device_name(self):
        msg = json.dumps({"command": "getFavoriteDeviceName"})
        await self.connection.send(msg)

    async def set_montage(self, channelnames: List):
        msg = json.dumps({
            "command": "setMontage",
            "channelnames": channelnames
            })
        await self.connection.send(msg)

    async def enable_data_grab_mode(self):
        msg = json.dumps({"command": "enableDataGrabMode"})
        await self.connection.send(msg)

    async def disable_data_grab_mode(self):
        msg = json.dumps({"command": "disableDataGrabMode"})
        await self.connection.send(msg)

    async def set_data_storage_time(self, value: int):
        msg = json.dumps({
            "command": "setDataStorageTime",
            "value": value
            })
        await self.connection.send(msg)

    async def get_data_storage_time(self):
        msg = json.dumps({"command": "getDataStorageTime"})
        await self.connection.send(msg)



    async def subscribe_rhytms(self):
        msg = json.dumps({"command": "rhythms"})
        while True:
            await self.connection.send(msg)
            await asyncio.sleep(1/self.freq)

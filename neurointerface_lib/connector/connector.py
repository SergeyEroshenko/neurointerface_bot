import asyncio
import json
from typing import List, Optional

from neurointerface_lib.core.observer import Subject
from ..core import BaseConnector


class Connector(BaseConnector):

    uri: str = "ws://127.0.0.1:1336"

    def __init__(
        self, device_id: str,
        rhytm_freq: int = 5,
        raw_freq: int = 125,
        parser: Optional[Subject] = None,
        window_size: int = 1,
    ) -> None:

        super().__init__()
        self.device_id = device_id
        self.rhytm_freq = rhytm_freq
        self.raw_freq = raw_freq
        self.window_size = window_size
        self.parser = parser
        self._data_storage_time = 10

        try:
            getattr(self.parser, 'raw_freq')
            setattr(self.parser, 'raw_freq', self.raw_freq)
        except AttributeError:
            pass

    async def handler(self):
        if self.parser is None:
            return await super().handler()
        else:
            async for message in self.connection:
                self._state = message
                self.parser.parse(self._state)
                # self.notify()

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
        print("disableDataGrabMode")
        await self.connection.send(msg)

    async def set_data_storage_time(self, value: int):
        self._data_storage_time = int(value)
        msg = json.dumps({
            "command": "setDataStorageTime",
            "value": value
            })
        await self.connection.send(msg)

    async def get_data_storage_time(self):
        msg = json.dumps({"command": "getDataStorageTime"})
        await self.connection.send(msg)

    async def get_filters(self):
        msg = json.dumps({"command": "getFilters"})
        await self.connection.send(msg)

    async def set_filters(self):
        msg = json.dumps({"command": "setFilters"})
        await self.connection.send(msg)

    async def set_lpf(self, value: int):
        msg = json.dumps({
            "command": "setLPF",
            "value": value
            })
        await self.connection.send(msg)

    async def set_bsf(self, value: int):
        msg = json.dumps({
            "command": "setBSF",
            "value": value
            })
        await self.connection.send(msg)

    async def set_hpf(self, value: int):
        msg = json.dumps({
            "command": "setHPF",
            "value": value
            })
        await self.connection.send(msg)

    async def filtered_data(self):
        msg = json.dumps({"command": "filteredData"})
        await self.connection.send(msg)

    async def grab_filtered_data(self):
        msg = json.dumps({"command": "grabFilteredData"})
        await self.connection.send(msg)

    async def raw_data(self):
        msg = json.dumps({"command": "rawData"})
        await self.connection.send(msg)

    async def grab_raw_data(self):
        msg = json.dumps({"command": "grabRawData"})
        while True:
            await self.connection.send(msg)
            await asyncio.sleep(self._data_storage_time)

    async def add_edf_annotation(self, duration: int, pos: int, text: str):
        msg = json.dumps({
            "command": "setHPF",
            "duration": duration,
            "pos": pos,
            "text": text
            })
        await self.connection.send(msg)

    async def spectrum(self):
        msg = json.dumps({"command": "spectrum"})
        while True:
            await self.connection.send(msg)
            await asyncio.sleep(self.window_size)

    async def spectrum_frequencies(self):
        msg = json.dumps({"command": "spectrumFrequencies"})
        while True:
            await self.connection.send(msg)
            await asyncio.sleep(self.window_size)

    async def rhythms(self):
        msg = json.dumps({"command": "rhythms"})
        while True:
            await self.connection.send(msg)
            await asyncio.sleep(1/self.rhytm_freq)

    async def rhythms_history(self):
        msg = json.dumps({"command": "rhythmsHistory"})
        try:
            while True:
                await self.connection.send(msg)
                await asyncio.sleep(self.window_size)
        except asyncio.CancelledError:
            pass

    async def meditation(self):
        msg = json.dumps({"command": "meditation"})
        while True:
            await self.connection.send(msg)
            await asyncio.sleep(1/self.rhytm_freq)

    async def meditation_history(self):
        msg = json.dumps({"command": "meditationHistory"})
        await self.connection.send(msg)

    async def concentration(self):
        msg = json.dumps({"command": "concentration"})
        while True:
            await self.connection.send(msg)
            await asyncio.sleep(1/self.rhytm_freq)

    async def concentration_history(self):
        msg = json.dumps({"command": "concentrationHistory"})
        await self.connection.send(msg)

    async def bci(self):
        msg = json.dumps({"command": "bci"})
        while True:
            await self.connection.send(msg)
            await asyncio.sleep(1/self.rhytm_freq)

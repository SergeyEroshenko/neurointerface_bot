import re
import json
import ciso8601
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional

# from neurointerface_lib.connector.connector import Connector
from typing import List
from ..core import Observer, Subject
from clickhouse_driver import Client


class Parser(Subject):
    def __init__(self) -> None:
        self._observers: List[Observer] = []
        self._state: Optional[pd.core.frame.DataFrame] = None

        self.names = ["alpha", "beta", "delta", "gamma", "theta"]
        self.rhythms_keys = [
            name + "_" + str(i) for i in range(8) for name in self.names
        ]

        self._raw_freq: Optional[int] = None
        # self._rhytm_freq: Optional[int] = None

    @property
    def raw_freq(self):
        return self._raw_freq

    @raw_freq.setter
    def raw_freq(self, val):
        self._raw_freq = val

    def _date_to_timestamp(self, date):
        date += "000"
        date_params = date.replace('-', '.').split('.')
        date_params = map(int, date_params)
        timestamp = int(datetime(*date_params).timestamp() * 1000)
        return timestamp

    def parse(self, message: str):
        json_dict = json.loads(message)
        channel = json_dict["command"]
        print(channel)
        if channel == "rhythms":
            data = [json_dict["rhythms"]]
            self._state = self.parse_rhythms(data, channel)
        elif channel == "rhythmshistory":
            data = json_dict["history"]
            self._state = self.parse_rhythms(data, channel)
        elif channel in ("grabrawdata", "rawdata"):
            data = json_dict["data"]
            end_time = self._date_to_timestamp(json_dict["time"])
            self._state = self.parse_raw(data, channel, end_time)

        if self._state is not None:
            self.notify()

    def parse_rhythms(self, data, channel):

        data_arrs = np.empty((0, 40))
        time_arr = np.array([]).astype(np.int64)
        for timestamp in data:
            t = timestamp[0]["t"]
            time_arr = np.append(time_arr, t)
            ts_data = np.array([])
            for channel_data in timestamp:
                ts_data = np.append(
                    ts_data, [channel_data[name] for name in self.names]
                )

            data_arrs = np.append(data_arrs, [ts_data], axis=0)

        parsed_data = pd.DataFrame(data_arrs, columns=self.rhythms_keys)
        parsed_data.insert(loc=0, column="timestamp", value=time_arr)
        parsed_data.name = channel

        return parsed_data

    def parse_raw(self, data, channel, end_time):

        start_time = end_time - int(len(data[0]) / self._raw_freq * 1000)
        step = int(1 / self._raw_freq * 1000)
        timestamp = list(range(start_time, end_time, step))

        columns = [f"EEG_{i}" for i in range(8)]
        df_dict = dict((col, vals) for col, vals in zip(columns, data))
        parsed_data = pd.DataFrame(df_dict)
        parsed_data.insert(loc=0, column="timestamp", value=timestamp)
        parsed_data.name = channel
        return parsed_data

    def set_endpoint(self, obj):
        # TODO: add obj type as Converter
        # TODO: add class Converter into core
        self.endpoint = obj

    def put_endpoint(self, data):
        self.endpoint.update

    def converte_timestamp(self, timestamp: str):
        timestamp = timestamp.replace("-", "T")
        timestamp = re.sub(r"\.", "-", timestamp, 2)
        timestamp = re.sub(r"\.", ":", timestamp, 2)
        timestamp_float = ciso8601.parse_datetime(timestamp).timestamp()
        return timestamp_float


class DBWriter(Observer):
    def __init__(self, client: Client, label: int):
        super().__init__()
        self.client = client
        self.label = label

        self.init_time = datetime.now().isoformat().split(".")[0]
        self.init_time = self.init_time.replace("-", "_").replace(":", "")

        self.table_params = f"{self.init_time}_label{self.label}"
        print("\nDBWriter start time: ", self.init_time)
        # self.header_rhythms = None
        # self.check_tables()

    def _get_headers(self, columns):
        time_type = " DateTime64(3, 'Europe/Moscow')"
        float_type = " Float32"
        headers_list = []
        for cname in columns:
            if cname == "timestamp":
                headers_list.append(cname + time_type)
            else:
                headers_list.append(cname + float_type)

        return ", ".join(headers_list)

    def _write_data(self, dataframe: pd.core.frame.DataFrame, headers: str):
        name = dataframe.name

        self.client.execute(
            (
                "CREATE TABLE IF NOT EXISTS "
                f"{self.table_params}_{name} "
                f"( {headers} ) "
                "ENGINE = MergeTree ORDER BY timestamp"
            )
        )
        self.client.insert_dataframe(
            f"INSERT INTO {self.table_params}_{name} VALUES", dataframe
        )

    def update(self, dataframe: pd.core.frame.DataFrame):
        headers = self._get_headers(dataframe.columns)
        self._write_data(dataframe, headers)

    # @staticmethod
    # def parse_rhythms(data):
    #     # print(len(data))
    #     # print(pd.DataFrame(data[0], index=[0]))
    #     row = list()
    #     for idx, ch_data in enumerate(data):
    #         timestamp = ch_data.pop('t')
    #         row.append(pd.DataFrame(ch_data, index=[idx]))
    #     timestamp /= 1000
    #     data = pd.concat(row).astype(np.float32).stack()
    #     data.index = data.index.to_flat_index()\
    #         .map(lambda x: f"{x[1]}_{x[0]}")
    #     df = data.to_frame().transpose()
    #     return df, timestamp

    # def parse_rhythms_history(self, data):
    #     parsed_data = pd.DataFrame()
    #     for time_point in data:
    #         time_point = pd.DataFrame(time_point)
    #         timestamp = time_point.loc[0, 't']
    #         time_point = time_point.drop('t', axis=1).stack()
    #         time_point.index = time_point.index.to_flat_index()\
    #             .map(lambda x: f"{x[1]}_{x[0]}")
    #         time_point.name = timestamp
    #         parsed_data = parsed_data.append(time_point)
    #     parsed_data.index.name = 'timestamp'
    #     return parsed_data

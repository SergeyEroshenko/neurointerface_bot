import re
import json
import ciso8601
from datetime import datetime
from typing import Dict
import pandas as pd
from ..core import Observer, Subject
from clickhouse_driver import Client


class Parser(Observer):

    def update(self, subject: Subject):
        state: str = subject._state
        message: Dict = json.loads(state)
        self.parse(message)

    def parse(self, message: Dict):
        channel = message["command"]
        if channel == "rhythms":
            pass

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
        self.init_time = datetime.now().isoformat().split('.')[0]\
            .replace('-', '_').replace(':', '')
        self.table_params = f"{self.init_time}_label{self.label}"
        print("DBWriter start time: ", self.init_time)
        # self.header_rhythms = None
        # self.check_tables()

    def update(self, subject: Subject):
        state: str = subject._state
        message: Dict = json.loads(state)
        self.parse(message)

    # def check_tables(self):
    #     rhythm_types = ['alpha', 'beta', 'delta', 'gamma', 'theta']
    #     channels = list(range(8))
    #     self.header_rhythms = ["timestamp DateTime('Europe/Moscow')"] + sum([
    #         list(map(lambda x: x + f"_{idx} Float32", rhythm_types))
    #         for idx in channels], [])

    #     self.client.execute((
    #         f"CREATE TABLE {self.table_params}_rhythms "
    #         "(" + ", ".join(self.header_rhythms) + ")"
    #         "ENGINE = MergeTree ORDER BY timestamp"
    #     ))

    def parse(self, message: Dict):
        channel = message["command"]
        # print(channel)
        if channel == "rhythms":
            data = message["rhythms"]
            data = self.parse_rhythms(data)
            self.client.execute((
                f"CREATE TABLE IF NOT EXISTS {self.table_params}_rhythms "
                "( timestamp DateTime('Europe/Moscow')"
                ", ".join(data.columns) + ")"
                "ENGINE = MergeTree ORDER BY timestamp"
            ))
            self.client.execute(
                f"INSERT INTO {self.table_params}_rhythms VALUES",
                data.to_dict('records')
                )
        elif channel == "rhythmshistory":
            try:
                data = message["history"]
            except Exception:                   # уточнить ошибку
                err = message['error']
                raise Exception(err)
            data = self.parse_rhythms_history(data)

            headers_list = ["timestamp DateTime64(3)"]\
                + [f"{name} Float32" for name in data.columns]
            header = ", ".join(headers_list)
            self.client.execute((
                "CREATE TABLE IF NOT EXISTS "
                f"{self.table_params}_rhythmsHistory "
                f"( {header} ) "
                "ENGINE = MergeTree ORDER BY timestamp"
            ))
            print(data)
            self.client.insert_dataframe(
                f"INSERT INTO {self.table_params}_rhythmsHistory VALUES",
                data.reset_index())

    @staticmethod
    def parse_rhythms(data):
        print(len(data))
        print(pd.DataFrame(data[0], index=[0]))
        # row = list()
        # for idx, ch_data in enumerate(data):
        #     timestamp = ch_data.pop('t')
        #     row.append(pd.DataFrame(ch_data, index=[idx]))
        # timestamp /= 1000
        # data = pd.concat(row).astype(np.float32).stack()
        # data.index = data.index.to_flat_index()\
        #     .map(lambda x: f"{x[1]}_{x[0]}")
        # data = np.append(
        #     np.array(timestamp).astype(str),
        #     data.astype(str).values
        #     )
        # data = ', '.join(data)
        return data

    def parse_rhythms_history(self, data):
        parsed_data = pd.DataFrame()
        for time_point in data:
            time_point = pd.DataFrame(time_point)
            timestamp = time_point.loc[0, 't']
            time_point = time_point.drop('t', axis=1).stack()
            time_point.index = time_point.index.to_flat_index()\
                .map(lambda x: f"{x[1]}_{x[0]}")
            time_point.name = timestamp
            parsed_data = parsed_data.append(time_point)
        parsed_data.index.name = 'timestamp'
        return parsed_data

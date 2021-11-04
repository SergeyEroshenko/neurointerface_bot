import re
import json
import ciso8601
from typing import Dict
from ..core import Observer, Subject


class Parser(Observer):

    def update(self, subject: Subject):
        message: str = subject._state
        message: Dict = json.loads(message)
        print(message)

    def converte_timestamp(self, timestamp: str) -> float:
        timestamp = timestamp.replace("-", "T")
        timestamp = re.sub("\.", "-", timestamp, 2)
        timestamp = re.sub("\.", ":", timestamp, 2)
        timestamp = ciso8601.parse_datetime(timestamp).timestamp()
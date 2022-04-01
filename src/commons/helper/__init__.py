import time
from .converter import candleToPandas


def getTimestamp() -> int:
    return int(time.time()*1000)
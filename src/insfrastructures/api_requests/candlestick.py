import pandas as pd
from src.commons import utils
from src.commons import helper
from src.domains.bases.baseRequest import BaseRequest
from src.domains.entities.requestEntity import RequestEntity
from src.commons.exceptions.requestError import RequestError


class CandleStick(BaseRequest):

    def __init__(self):
        entity = RequestEntity(
            resourceApi=utils.BINANCE,
            path="api/v1/klines",
            method=utils.GET
        )
        super().__init__(requestEntity=entity)

    def setParams(self, symbol=None, interval=None, startTime=None, endTime=None, limit=500):
        self.params["symbol"] = symbol
        self.params["interval"] = interval
        self.params["startTime"] = startTime
        self.params["endTime"] = endTime
        self.params["limit"] = limit
        for key, value in self.params.copy().items():
            if value is None:
                self.params.pop(key)

    def send(self, *args, **kwargs) -> pd.DataFrame:
        req = self.request()
        if req.status_code not in [200, 201]:
            raise RequestError(f"{self.__class__.__name__}")
        return helper.candleToPandas(req.json())

from src.commons import utils
from src.commons.helper import getTimestamp
from src.domains.bases.baseRequest import BaseRequest
from src.domains.entities.requestEntity import RequestEntity
from src.commons.exceptions.requestError import RequestError


class AllOrder(BaseRequest):

    def __init__(self):
        entity = RequestEntity(
            resourceApi=utils.TOKO_CRYPTO,
            path="open/v1/orders",
            method=utils.GET
        )
        super().__init__(requestEntity=entity)

    def setParams(self, symbol=None, tType=None, side=None,
                  startTime=None, endTime=None, fromId=None,
                  direct=None, limit=None,
                  recvWindow=5000, timestamp=getTimestamp()):
        self.params["symbol"] = symbol
        self.params["type"] = tType
        self.params["side"] = side
        self.params["startTime"] = startTime
        self.params["endTime"] = endTime
        self.params["fromId"] = fromId
        self.params["direct"] = direct
        self.params["limit"] = limit
        self.params["recvWindow"] = recvWindow
        self.params["timestamp"] = timestamp
        for key, value in self.params.copy().items():
            if value is None:
                self.params.pop(key)

    def send(self, *args, **kwargs):
        req = self.request()
        if req.status_code not in [200, 201]:
            raise RequestError(f"{self.__class__.__name__}")
        return req.json()["data"]
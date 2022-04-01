from src.commons import utils
from src.domains.bases.baseRequest import BaseRequest
from src.domains.entities.requestEntity import RequestEntity
from src.commons.helper import getTimestamp
from src.commons.exceptions.requestError import RequestError


class NewOCO(BaseRequest):

    def __init__(self):
        entity = RequestEntity(
            resourceApi=utils.TOKO_CRYPTO,
            path="open/v1/orders/oco",
            method=utils.POST,
        )
        super().__init__(requestEntity=entity)

    def setParams(self, symbol=None, listClientId=None, side=None,
                  quantity=None, limitClientId=None, price=None,
                  stopClientId=None, stopPrice=None, stopLimitPrice=None,
                  recvWindow=5000, timestamp=getTimestamp()):
        self.params["symbol"] = symbol
        self.params["listClientId"] = listClientId
        self.params["side"] = side
        self.params["quantity"] = quantity
        self.params["limitClientId"] = limitClientId
        self.params["price"] = price
        self.params["stopClientId"] = stopClientId
        self.params["stopPrice"] = stopPrice
        self.params["stopLimitPrice"] = stopLimitPrice
        self.params["recvWindow"] = recvWindow
        self.params["timestamp"] = timestamp
        for key, value in self.params.copy().items():
            if value is None:
                self.params.pop(key)

    def send(self, *args, **kwargs):
        req = self.request()
        if req.status_code not in [200, 201]:
            raise RequestError(f"{self.__class__.__name__}")
        return req.json()
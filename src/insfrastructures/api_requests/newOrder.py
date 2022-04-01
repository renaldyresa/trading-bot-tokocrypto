from src.commons import utils
from src.commons.helper import getTimestamp
from src.domains.bases.baseRequest import BaseRequest
from src.domains.entities.requestEntity import RequestEntity
from src.commons.exceptions.requestError import RequestError


class NewOrder(BaseRequest):

    def __init__(self):
        entity = RequestEntity(
            resourceApi=utils.TOKO_CRYPTO,
            path="open/v1/orders",
            method=utils.POST
        )
        super().__init__(requestEntity=entity)

    def setParams(self, symbol=None, side=None, tType=None,
                  quantity=None, quoteOrderQty=None, price=None,
                  clientId=None, stopPrice=None, icebergQty=None,
                  recvWindow=5000, timestamp=getTimestamp()):
        self.params["symbol"] = symbol
        self.params["side"] = side
        self.params["type"] = tType
        self.params["quantity"] = quantity
        self.params["quoteOrderQty"] = quoteOrderQty
        self.params["price"] = price
        self.params["clientId"] = clientId
        self.params["stopPrice"] = stopPrice
        self.params["icebergQty"] = icebergQty
        self.params["recvWindow"] = recvWindow
        self.params["timestamp"] = timestamp
        for key, value in self.params.copy().items():
            if value is None:
                self.params.pop(key)

    def send(self, *args, **kwargs):
        req = self.request()
        if req.status_code not in [200, 201]:
            raise RequestError(f"{self.__class__.__name__}")
        return req.json()["data"]["orderId"]

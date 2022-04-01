from src.commons import utils
from src.domains.bases.baseRequest import BaseRequest
from src.domains.entities.requestEntity import RequestEntity
from src.commons.exceptions.requestError import RequestError


class OrderBook(BaseRequest):

    def __init__(self):
        entity = RequestEntity(
            resourceApi=utils.TOKO_CRYPTO,
            path="open/v1/market/depth",
            method=utils.GET
        )
        super().__init__(requestEntity=entity)

    def setParams(self, symbol=None, limit=100):
        self.params["symbol"] = symbol
        self.params["limit"] = limit
        for key, value in self.params.copy().items():
            if value is None:
                self.params.pop(key)

    def send(self, *args, **kwargs):
        req = self.request()
        if req.status_code not in [200, 201]:
            raise RequestError(f"{self.__class__.__name__}")
        return req.json().get("data", {})

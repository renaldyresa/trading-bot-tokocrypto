from src.commons import utils
from src.domains.bases.baseRequest import BaseRequest
from src.domains.entities.requestEntity import RequestEntity
from src.commons.helper import getTimestamp
from src.commons.exceptions.requestError import RequestError


class AccountInformation(BaseRequest):

    def __init__(self):
        entity = RequestEntity(
            resourceApi=utils.TOKO_CRYPTO,
            path="open/v1/account/spot",
            method=utils.GET
        )
        super().__init__(requestEntity=entity)

    def setParams(self, recvWindow=5000, timestamp=getTimestamp()):
        self.params["recvWindow"] = recvWindow
        self.params["timestamp"] = timestamp
        for key, value in self.params.items():
            if value is None:
                self.params.pop(key)

    def send(self, *args, **kwargs):
        req = self.request()
        if req.status_code not in [200, 201]:
            raise RequestError(f"{self.__class__.__name__}")
        return req.json()
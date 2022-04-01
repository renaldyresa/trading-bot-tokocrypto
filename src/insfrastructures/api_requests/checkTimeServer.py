from src.commons import utils
from src.domains.bases.baseRequest import BaseRequest
from src.domains.entities.requestEntity import RequestEntity
from src.commons.exceptions.requestError import RequestError


class CheckTimeServer(BaseRequest):

    def __init__(self):
        entity = RequestEntity(
            resourceApi=utils.TOKO_CRYPTO,
            path="open/v1/common/time",
            method=utils.GET
        )
        super().__init__(requestEntity=entity)

    def setParams(self, **kwargs):
        pass

    def send(self, *args, **kwargs):
        response = self.request()
        if req.status_code not in [200, 201]:
            raise RequestError(f"{self.__class__.__name__}")
        print(response.json())

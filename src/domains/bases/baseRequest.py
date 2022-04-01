import os
import requests
from abc import abstractmethod
from src.domains.bases.baseCoin import BaseCoin
from src.domains.entities.requestEntity import RequestEntity
from src.commons.exceptions.requestError import RequestError
from src.security import generateHmac


class BaseRequest:

    def __init__(self, requestEntity: RequestEntity):
        self.__requestEntity: RequestEntity = requestEntity
        self.__coin: BaseCoin = None
        self.params: dict = {}
        self.headers: dict = {
            "X-MBX-APIKEY": os.getenv("API-KEY"),
        }

    @property
    def coin(self):
        return self.__coin

    @coin.setter
    def coin(self, coin: BaseCoin):
        self.__coin = coin

    def setHeaders(self, **kwargs):
        self.headers.update(kwargs)

    def setSignature(self):
        signature = generateHmac(self.params.copy())
        self.params["signature"] = signature

    def request(self) -> requests.Response:
        try:
            req = requests.request(
                method=self.__requestEntity.method,
                url=f"{self.__requestEntity.resourceApi}/{self.__requestEntity.path}",
                params=self.params,
                headers=self.headers
            )
        except Exception as e:
            raise RequestError
        return req

    @abstractmethod
    def setParams(self, **kwargs):
        pass

    @abstractmethod
    def send(self, *args, **kwargs):
        pass



from src.commons.exceptions.error import BaseError


class RequestError(BaseError):

    def __init__(self, message=""):
        super().__init__(f"Request failed({message})")
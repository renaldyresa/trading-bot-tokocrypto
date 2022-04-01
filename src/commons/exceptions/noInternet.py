from src.commons.exceptions.error import BaseError


class NoInternet(BaseError):

    def __init__(self, message=""):
        super().__init__(f"No Connection Internet ({message})")
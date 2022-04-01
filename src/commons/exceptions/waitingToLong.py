from src.commons.exceptions.error import BaseError


class WaitingToLong(BaseError):

    def __init__(self, message=""):
        super().__init__(f"Waiting To Log ({message})")




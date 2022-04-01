from dataclasses import dataclass


@dataclass
class RequestEntity:
    resourceApi: str
    path: str
    method: str

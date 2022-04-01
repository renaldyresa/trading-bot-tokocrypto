from dataclasses import dataclass


@dataclass
class OrderEntity:
    id: str
    coin_name: str
    timestamp_buy: int
    price_buy: str
    timestamp_sell: int
    price_sell: str

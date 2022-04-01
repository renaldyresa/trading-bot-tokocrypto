import json
import os
from datetime import datetime
from dataclasses import asdict
from src.domains.entities.orderEntity import OrderEntity
from src.insfrastructures.api_requests.queryOrder import QueryOrder


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def createTransaction(coin, priceBuy, quantityBuy, priceSell, quantitySell):
    today = datetime.today().strftime("%Y-%m-%d")
    path = os.path.join(ROOT_DIR, f"history/{today}.txt")
    profit = float(priceSell)*float(quantitySell) - float(priceBuy)*float(quantityBuy)
    with open(path, "a+") as f:
        text = f"{coin}||{priceBuy}||{quantityBuy}||{priceSell}||{quantitySell}||{profit}\n"
        f.write(text)


def getOrders() -> list:
    path = os.path.join(ROOT_DIR, f"orders.json")
    with open(path, "r+") as f:
        data = json.load(f)
        orders = data.get("data", [])
        results = []
        for order in orders:
            orderEntity = OrderEntity(
                id=order.get("id"),
                coin_name=order.get("coin_name"),
                timestamp_buy=order.get("timestamp_buy"),
                price_buy=order.get("price_buy"),
                timestamp_sell=order.get("timestamp_sell"),
                price_sell=order.get("price_sell")

            )
            queryOrder = QueryOrder()
            queryOrder.setParams(orderId=orderEntity.id)
            queryOrder.setSignature()
            response = queryOrder.send()
            if response["status"] in [0, 1]:
                results.append(orderEntity)
        return results


def addOrder(orderEntity: OrderEntity):
    orders = getOrders()
    orders.append(orderEntity)
    serializeOrders = []
    for order in orders:
        serializeOrders.append(asdict(order))

    path = os.path.join(ROOT_DIR, f"orders.json")

    with open(path, "w") as f:
        f.write(json.dumps({"data": serializeOrders}))


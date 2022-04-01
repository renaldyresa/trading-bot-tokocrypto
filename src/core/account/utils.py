import time
from src.insfrastructures.api_requests.queryOrder import QueryOrder
from src.commons.exceptions.waitingToLong import WaitingToLong


def waiting(orderId, duration, totalDuration, orderIdTakeProfit=None, message=""):
    i = 0
    while True:
        time.sleep(duration)
        queryOrder = QueryOrder()
        queryOrder.setParams(
            orderId=orderId,
        )
        queryOrder.setSignature()
        response = queryOrder.send()
        if response["status"] == 2 or response["status"] == "2":
            return response

        if orderIdTakeProfit is not None:
            queryOrder = QueryOrder()
            queryOrder.setParams(
                orderId=orderIdTakeProfit,
            )
            queryOrder.setSignature()
            response = queryOrder.send()
            if response["status"] == 2 or response["status"] == "2":
                return response

        if i > totalDuration:
            raise WaitingToLong(message)
        i += 1
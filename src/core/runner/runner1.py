import asyncio
import random
import time

from src.commons import utils
from src.domains.bases.baseCoin import BaseCoin
from src.core.tradinglines.movingAverage import MovingAverage
from src.core.algorithms.algo1 import Algo1
from src.insfrastructures.coins import LIST_COINS
from src.core.account.calculate import getQuantityAndOrderBookForBuy, getQuantityAndOrderBookForSell
from src.insfrastructures.api_requests.newOrder import NewOrder
from src.insfrastructures.api_requests.queryOrder import QueryOrder
from src.insfrastructures.api_requests.allOrder import AllOrder
from src.insfrastructures.api_requests.newOco import NewOCO
from src.insfrastructures.api_requests.cancelOrder import CancelOrder
from src.transactions import createTransaction


async def calculate(coin: BaseCoin):
    movingAverage = MovingAverage(
        symbol=coin.toUSDT(False),
        ma=[20, 100],
        interval="30m"
    )
    movingAverage.setMovingAverage()
    algo = Algo1(ma=movingAverage)
    isBuy = algo.isBuy()
    if isBuy:
        movingAverage.createChart()
    return isBuy, coin


def waiting(orderId, duration, totalDuration):
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
            break
        if i > totalDuration:
            raise Exception("wait to long")
        i += 1


def buyCoin(coin: BaseCoin):
    quantity, resOrderBook = getQuantityAndOrderBookForBuy(coin=coin, percentWallet=100)
    newOrder = NewOrder()
    newOrder.setParams(
        symbol=coin.toUSDT(),
        side=utils.BUY,
        tType=1,
        price=resOrderBook["asks"][1][0],
        quantity=quantity,
    )
    print("=======================")
    print(f"COIN : {coin.toUSDT()} || quantity : {quantity} || price : {resOrderBook['asks'][1][0]} || side : BUY")
    print("=======================")
    newOrder.setSignature()
    orderId = newOrder.send()
    return orderId, resOrderBook["asks"][1][0], quantity


def setOCO(coin: BaseCoin):
    quantity, orderbook = getQuantityAndOrderBookForSell(coin, percentWallet=100, limit=100)

    newOCO = NewOCO()
    newOCO.setParams(
        symbol=coin.toUSDT(),
        side=utils.SELL,
        quantity=quantity,
        price=orderbook["asks"][20][0],
        stopPrice=orderbook["bids"][20][0],
        stopLimitPrice=orderbook["bids"][22][0]
    )
    newOCO.setSignature()
    newOCO.send()

    print("=======================")
    print(f"COIN : {coin.toUSDT()} || quantity : {quantity} || price : {orderbook['asks'][40][0]} || cutLoss : {orderbook['bids'][25][0]} || side : SELL")
    print("=======================")


async def run():

    tasks = []
    for coin in LIST_COINS:
        tasks.append(asyncio.create_task(calculate(coin())))

    coins = []
    for task in tasks:
        isBuy, coin = await task
        if isBuy:
            coins.append(coin)

    if not coins:
        raise Exception("No to buy")

    coin = random.choice(coins)

    orderId, priceBuy, quantityBuy = buyCoin(coin)
    try:
        waiting(orderId, 30, 20)
    except Exception as e:
        cancelOrder = CancelOrder()
        cancelOrder.setParams(
            orderId=orderId
        )
        cancelOrder.setSignature()
        cancelOrder.send()
        return

    setOCO(coin)
    allOrder = AllOrder()
    allOrder.setParams(
        symbol=coin.toUSDT(),
        side=utils.SELL
    )
    allOrder.setSignature()
    response = allOrder.send()
    orderId = response["list"][0]["orderId"]

    try:
        waiting(orderId, 60, 60)
    except Exception as e:
        cancelOrder = CancelOrder()
        cancelOrder.setParams(
            orderId=orderId
        )
        cancelOrder.setSignature()
        cancelOrder.send()


        return

    queryOr = QueryOrder()
    queryOr.setParams(orderId=orderId)
    queryOr.setSignature()
    resQueryOrder = queryOr.send()
    priceSell = resQueryOrder["price"]
    quantitySell = resQueryOrder["origQty"]


    print("RUNNER ENDED")
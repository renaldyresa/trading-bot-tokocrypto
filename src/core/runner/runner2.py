import asyncio
import random
import time

from src.commons import utils
from src.domains.bases.baseCoin import BaseCoin
from src.core.tradinglines.movingAverage import MovingAverage
from src.core.tradinglines.macd import MACD
from src.core.algorithms.algo1 import Algo1
from src.core.algorithms.algo2 import Algo2
from src.core.algorithms.algo3 import Algo3
from src.core.algorithms.algo5 import Algo5
from src.insfrastructures.coins import LIST_COINS
from src.core.account.calculate import getQuantityAndOrderBookForBuy, getQuantityAndOrderBookForSell
from src.insfrastructures.api_requests.newOrder import NewOrder
from src.insfrastructures.api_requests.queryOrder import QueryOrder
from src.insfrastructures.api_requests.allOrder import AllOrder
from src.insfrastructures.api_requests.newOco import NewOCO
from src.insfrastructures.api_requests.cancelOrder import CancelOrder
from src.transactions import createTransaction
from src.commons.exceptions.waitingToLong import WaitingToLong
from src.commons.exceptions.requestError import RequestError


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


async def calculate(coin: BaseCoin, ma=(20, 100), interval="1h", limit=400):
    movingAverage = MovingAverage(
        coin=coin,
        ma=ma,
        interval=interval,
        limit=limit
    )
    movingAverage.setMovingAverage()
    algo1 = Algo1(ma=movingAverage)
    algo2 = Algo2(ma=movingAverage)
    algo5 = Algo5(coin=coin)
    if algo1.isBuy() and algo2.isBuy() and algo5.isBuy():
        movingAverage.createChart()
        return True, coin
        # macd = MACD(
        #     coin=coin,
        #     interval=interval,
        #     limit=limit
        # )
        # macd.setMACD()
        # # macd.createChart()
        # algo3 = Algo3(macd=macd)
        # if algo3.isBuy():
        #     # movingAverage.createChart()
        #     macd.createChart(movingAverage)
        #     return True, coin
    return False, coin


class Runner2:

    def __init__(self, coin: BaseCoin, percentWalletBuy=90):
        self.__coin = coin
        self.__percentWalletBuy = percentWalletBuy
        self.__priceBuy = None
        self.__quantityBuy = None
        self.__priceSell = None
        self.__quantitySell = None
        self.__orderBookBuy = None

    def buyCoin(self):
        self.__quantityBuy, self.__orderBookBuy = getQuantityAndOrderBookForBuy(
            coin=self.__coin,
            percentWallet=self.__percentWalletBuy
        )
        self.__priceBuy = self.__orderBookBuy["asks"][2][0]
        newOrder = NewOrder()
        newOrder.setParams(
            symbol=self.__coin.toUSDT(),
            side=utils.BUY,
            tType=1,
            price=self.__priceBuy,
            quantity=self.__quantityBuy
        )
        newOrder.setSignature()
        orderId = newOrder.send()
        print("=======================")
        print(f"COIN : {self.__coin.toUSDT()} || quantity : {self.__quantityBuy} || price : {self.__priceBuy} || side : BUY")
        print("=======================")

        try:
            waiting(orderId=orderId, duration=15, totalDuration=40, message="for buy")
        except Exception as e:
            if isinstance(e, WaitingToLong) or isinstance(e, RequestError):
                cancelOrder = CancelOrder()
                cancelOrder.setParams(
                    orderId=orderId
                )
                cancelOrder.setSignature()
                cancelOrder.send()
            else:
                raise e

    def sellCoin(self):
        quantity, orderBook = getQuantityAndOrderBookForSell(
            coin=self.__coin,
            percentWallet=100
        )
        price = orderBook["bids"][1][0]
        newOrder = NewOrder()
        newOrder.setParams(
            symbol=self.__coin.toUSDT(),
            side=utils.SELL,
            tType=1,
            price=price,
            quantity=quantity
        )
        newOrder.setSignature()
        orderId = newOrder.send()
        print("=======================")
        print(f"COIN : {self.__coin.toUSDT()} || quantity : {quantity} || price : {price} || side : SELL")
        print("=======================")

        try:
            response = waiting(orderId=orderId, duration=10, totalDuration=30)
            self.__priceSell = response["price"]
            self.__quantitySell = response["origQty"]
        except Exception as e:
            if isinstance(e, WaitingToLong) or isinstance(e, RequestError):
                cancelOrder = CancelOrder()
                cancelOrder.setParams(
                    orderId=orderId
                )
                cancelOrder.setSignature()
                cancelOrder.send()

                self.sellCoin()
            else:
                raise e

    def setOco(self, iPrice=25, iStopPrice=20):
        quantity, orderBook = getQuantityAndOrderBookForSell(
            coin=self.__coin,
            percentWallet=100,
            limit=100
        )

        price = orderBook["asks"][iPrice][0]
        stopPrice = orderBook["bids"][iStopPrice][0]
        stopLimitPrice = orderBook["bids"][iStopPrice+2][0]

        newOco = NewOCO()
        newOco.setParams(
            symbol=self.__coin.toUSDT(),
            side=utils.SELL,
            quantity=quantity,
            price=price,
            stopPrice=stopPrice,
            stopLimitPrice=stopLimitPrice
        )
        newOco.setSignature()
        newOco.send()

        print("=======================")
        print(f"COIN : {self.__coin.toUSDT()} || quantity : {quantity} || takeProfit : {price} || cutLoss : {stopLimitPrice} || side : SELL")
        print("=======================")

        allOrder = AllOrder()
        allOrder.setParams(
            symbol=self.__coin.toUSDT(),
            side=utils.SELL
        )
        allOrder.setSignature()
        resAllOrder = allOrder.send()
        orderIdCutLoss = resAllOrder["list"][0]["orderId"]
        orderIdTakeProfit = resAllOrder["list"][1]["orderId"]
        try:
            response = waiting(
                orderId=orderIdCutLoss,
                duration=60,
                totalDuration=60,
                orderIdTakeProfit=orderIdTakeProfit
            )
            self.__priceSell = response["price"]
            self.__quantitySell = response["origQty"]
        except Exception as e:
            if isinstance(e, WaitingToLong) or isinstance(e, RequestError):
                cancelOrder = CancelOrder()
                cancelOrder.setParams(
                    orderId=orderIdCutLoss
                )
                cancelOrder.setSignature()
                cancelOrder.send()

                self.sellCoin()
            else:
                raise e

    def log(self):
        createTransaction(
            coin=self.__coin.toUSDT(),
            priceBuy=self.__priceBuy,
            quantityBuy=self.__quantityBuy,
            priceSell=self.__priceSell,
            quantitySell=self.__quantitySell
        )


async def run():
    tasks = []
    for coin in LIST_COINS:
        tasks.append(asyncio.create_task(calculate(
            coin=coin(),
            ma=(20, 100),
            interval="30m"
        )))

    # return

    coins = []
    for task in tasks:
        isBuy, coin = await task
        if isBuy:
            coins.append(coin)

    if len(coins) == 0:
        print("Nothing coin to buy")
        time.sleep(60*5)
        return True

    coin = random.choice(coins)

    try:
        runner = Runner2(coin=coin, percentWalletBuy=100)
        runner.buyCoin()
        runner.setOco(iPrice=30, iStopPrice=28)
        runner.log()
    except Exception as e:
        raise e
        return False
    return True







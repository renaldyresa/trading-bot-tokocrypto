import asyncio
import random
import time
from src.commons import utils
from src.domains.bases.baseCoin import BaseCoin
from src.core.tradinglines.macd import MACD
from src.core.tradinglines.movingAverage import MovingAverage
from src.core.algorithms.algo1 import Algo1
from src.core.algorithms.algo2 import Algo2
from src.core.algorithms.algo3 import Algo3
from src.core.algorithms.algo4 import Algo4
from src.core.algorithms.algo5 import Algo5
from src.domains.entities.orderEntity import OrderEntity
from src.insfrastructures import coins
from src.transactions import createTransaction, getOrders, addOrder
from src.core.account.calculate import getQuantityAndOrderBookForSell, getQuantityAndOrderBookForBuy
from src.commons.helper import getTimestamp
from src.insfrastructures.api_requests.newOrder import NewOrder
from src.insfrastructures.api_requests.cancelOrder import CancelOrder
from src.insfrastructures.api_requests.allOrder import AllOrder
from src.insfrastructures.api_requests.newOco import NewOCO
from src.commons.exceptions.waitingToLong import WaitingToLong
from src.commons.exceptions.requestError import RequestError
from src.core.account.utils import waiting
from src.core.tradinglines.supportAndResistance import SupportResistance


duration_buy, total_duration_buy = 15, 40
duration_sell, total_duration_sell = 10, 30
duration_oco, total_duration_oco = 60, 60


class Runner3:

    def __init__(self, coin: BaseCoin, percentWalletBuy=90):
        self.__coin = coin
        self.__percentWalletBuy = percentWalletBuy
        self.__priceBuy = None
        self.__timestampBuy = None
        self.__quantityBuy = None
        self.__priceSell = None
        self.__timestampSell = None
        self.__quantitySell = None
        self.__orderBookBuy = None

    def buyCoin(self):
        self.__quantityBuy, self.__orderBookBuy = getQuantityAndOrderBookForBuy(
            coin=self.__coin,
            percentWallet=self.__percentWalletBuy
        )
        self.__priceBuy = self.__orderBookBuy['asks'][2][0]
        self.__timestampBuy = getTimestamp()
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
        print(f"ORDERID: {orderId} || COIN : {self.__coin.toUSDT()} || quantity : {self.__quantityBuy} || price : {self.__priceBuy} || side : BUY")
        print("=======================")
        try:
            # addOrder(OrderEntity(
            #     id=orderId,
            #     coin_name=self.__coin.toUSDT(),
            #     timestamp_buy=self.__timestampBuy,
            #     price_buy=self.__priceBuy,
            #     timestamp_sell=None,
            #     price_sell=None
            # ))
            waiting(
                orderId=orderId,
                duration=duration_buy,
                totalDuration=total_duration_buy,
                orderIdTakeProfit=None,
                message="FOR BUY"
            )
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
        print(f"OrderId: {orderId} || COIN : {self.__coin.toUSDT()} || quantity : {quantity} || price : {price} || side : SELL")
        print("=======================")
        try:
            response = waiting(orderId=orderId, duration=duration_sell, totalDuration=total_duration_sell)
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
        stopLimitPrice = orderBook["bids"][iStopPrice + 2][0]

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
        print(
            f"COIN : {self.__coin.toUSDT()} || quantity : {quantity} || takeProfit : {price} || cutLoss : {stopLimitPrice} || side : SELL")
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
                duration=duration_oco,
                totalDuration=total_duration_oco,
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


async def calculate(coin: BaseCoin, ma=[20, 100], interval="1h", limit=500):
    movingAverage = MovingAverage(
        coin=coin,
        ma=ma,
        interval=interval,
        limit=limit
    )
    movingAverage.setMovingAverage()

    macd = MACD(coin, interval, limit)
    macd.setMACD()

    algo1 = Algo1(ma=movingAverage)
    algo2 = Algo2(ma=movingAverage)
    # algo3 = Algo3(macd=macd)
    # algo4 = Algo4(coin=coin)
    algo5 = Algo5(coin=coin)

    # results = [algo1.isBuy(), algo2.isBuy()]
    # print(f"coin:: {coin.toUSDT()} - {results}")
    if algo1.isBuy() and algo2.isBuy():
        sp = SupportResistance(movingAverage)
        sp.set()
        print(f"{coin.toUSDT()}:::: {sp.getSupportAndResistance()}")
        movingAverage.createChart()
        return True, coin
    return False, coin


async def run():
    orders = getOrders()
    if len(orders) > 0:
        print(orders)
        return
    # return
    tasks = []
    for coin in coins.LIST_COINS:
        tasks.append(asyncio.create_task(calculate(
            coin=coin(),
            ma=[20, 80],
            interval="1d",
            limit=500
        )))

    buyCoins = []
    for task in tasks:
        isBuy, coin = await task
        if isBuy:
            buyCoins.append(coin)



    # if len(buyCoins) == 0:
    #     print("Nothing coin to buy")
    #     time.sleep(60 * 5)
    #     return True
    #
    # coin = random.choice(buyCoins)
    #
    # try:
    #     runner = Runner3(coin=coin, percentWalletBuy=100)
    #     runner.buyCoin()
    #     runner.setOco(iPrice=30, iStopPrice=28)
    #     runner.log()
    # except Exception as e:
    #     raise e
    #     return False
    # return True







import asyncio
import json

from dotenv import load_dotenv
from src.insfrastructures.api_requests.checkTimeServer import CheckTimeServer
from src.insfrastructures.api_requests.accountInformation import AccountInformation
from src.insfrastructures.api_requests.candlestick import CandleStick
from src.insfrastructures import coins
from src.commons import utils

load_dotenv()


def testCheckTimeServer():
    instance = CheckTimeServer()
    instance.send()


def testAccountInformation():
    ins = AccountInformation()
    ins.setParams()
    ins.setSignature()
    ins.send()


def testCandleStick():
    coin = coins.ADACoin()
    ins = CandleStick()
    ins.setParams(
        symbol=coin.toBIDR(False),
        interval="1h",
        limit=10
    )
    ins.send()

from src.core.tradinglines.movingAverage import MovingAverage
def testMa20Ma501H():
    coin = coins.KEYCoin()
    m = MovingAverage(coin=coin, ma=[20, 80], interval="1d")
    m.setMovingAverage()
    m.createChart()

from src.core.algorithms.algo1 import Algo1
def testAlgo1():
    coin = coins.TFUELCoin()
    movingAverage = MovingAverage(
        coin=coin,
        ma=[20, 100],
    )
    movingAverage.setMovingAverage()
    movingAverage.createChart()
    algo = Algo1(ma=movingAverage)
    print(algo.isBuy())


from src.insfrastructures.api_requests.orderbook import OrderBook
def testOrderBook():
    coin = coins.ADACoin()
    orderBook = OrderBook()
    orderBook.setParams(
        symbol=coin.toUSDT(),
        limit=10,
    )
    resp = orderBook.send()
    print(resp)

from src.insfrastructures.api_requests.assetInformation import AssetInformation
def testAssetInformation():
    coin = coins.ADACoin()
    assetInformation = AssetInformation()
    assetInformation.setParams(
        asset="USDT",
    )
    assetInformation.setSignature()
    res = assetInformation.send()
    print(res)


from src.insfrastructures.api_requests.newOrder import NewOrder

def testNewOrder():
    coin = coins.ADACoin()
    orderBook = OrderBook()
    orderBook.setParams(
        symbol=coin.toUSDT(),
        limit=10
    )
    resOrderBook = orderBook.send()
    price = resOrderBook["asks"][0][0]

    newOrder = NewOrder()
    newOrder.setParams(
        symbol=coin.toUSDT(),
        side=1,
        tType=1,
        quantity="7",
        price=price
    )
    newOrder.setSignature()
    newOrder.send()


from src.core.account.calculate import getQuantityAndOrderBookForSell, getQuantityAndOrderBookForBuy

def testQuantityForSell():
    coin = coins.ADACoin()
    quantity = getQuantityAndOrderBookForSell(coin=coin)
    print(quantity)

def testQuantityForBuy():
    coin = coins.CFXCoin()
    quantity, orderbook = getQuantityAndOrderBookForBuy(coin)
    print(quantity)
    print(orderbook)


from src.insfrastructures.api_requests.newOco import NewOCO

def testNewOCO():
    coin = coins.ALPHACoin()

    quantity, orderbook = getQuantityAndOrderBookForSell(coin, percentWallet=100, limit=50)

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
    print(newOCO.send())

from src.core.runner import runner1

from src.insfrastructures.api_requests.allOrder import AllOrder

def testAllOrder():
    coin = coins.ALPHACoin()
    allOrder = AllOrder()
    allOrder.setParams(
        symbol=coin.toUSDT(),
        tType=1
    )
    allOrder.setSignature()
    allOrder.send()


from src.insfrastructures.api_requests.queryOrder import QueryOrder

def testQueryOrder():
    queryOrder = QueryOrder()
    queryOrder.setParams(orderId="56595181")
    queryOrder.setSignature()
    print(queryOrder.send())

from src.insfrastructures.api_requests.cancelOrder import CancelOrder

def testCancelOrder():
    cancelOrder = CancelOrder()
    cancelOrder.setParams(
        orderId="56837662",
    )
    cancelOrder.setSignature()
    cancelOrder.send()


from src.core.algorithms.algo2 import Algo2

def testAlgo2():
    coin = coins.ADACoin()
    movingAverage = MovingAverage(
        coin=coin,
        ma=[20, 100],
        interval="4h"
    )
    movingAverage.setMovingAverage()
    movingAverage.createChart()
    algo = Algo2(ma=movingAverage)
    print(algo.isBuy())

from src.core.runner import runner2

def testRunner2():
    # while True:
        print("RUNNER START")
        asyncio.run(runner2.run())

        print("RUNNER ENDED")


from src.core.tradinglines.macd import MACD

def testMacd():
    coin = coins.ATACoin()
    macd = MACD(
        coin=coin,
        interval="15m",
        limit=500
    )

    macd.setMACD()
    macd.createChart()

from src.core.algorithms.algo3 import Algo3

def testAlgo3():
    i = 0
    for tcoin in coins.LIST_COINS:
        coin = tcoin()
        macd = MACD(
            coin=coin,
            interval="1h",
            limit=100
        )
        macd.setMACD()
        macd.createChart()
        algo = Algo3(macd=macd)
        if algo.isBuy():
            print("beli: ", coin.toUSDT())
        else:
            print("tidak beli: ", coin.toUSDT())
        i += 1
        if i > 20:
            break


from src.core.algorithms.algo4 import Algo4

def testAlgo4():
    i = 0
    coin = coins.GRTCoin()
    # for coin in coins.LIST_COINS[17:]:
    algo4 = Algo4(coin)
    algo4.isBuy()
    i += 1
    print(coin.symbol)
    # break
    # if i > 10:
    #     break

from src.transactions import getOrders

# def testGetOrder():
#     getOrders()


from src.domains.entities.orderEntity import OrderEntity
from src.transactions import addOrder
from dataclasses import asdict

# def testOrderEntity():
#     orderEntity = OrderEntity(
#         id="1234234",
#         coinName="ADA",
#         timestamp=1234324
#     )
#     addOrder(orderEntity)
#     # print(json.dumps(asdict(orderEntity)))

from src.core.runner import runner3

def testRunner3():
    while True:
        print("RUNNER START")
        asyncio.run(runner3.run())
        print("RUNNER ENDED")
        break

from src.core.algorithms.algo5 import Algo5

def testAlgo5():
    coin = coins.ONECoin()
    algo = Algo5(coin)
    algo.isBuy()

from src.transactions import getOrders, addOrder

def testGetOrders():
    print(getOrders())


def testAddOrder():
    orderEntity = OrderEntity(
        id="1234",
        coin_name="ADA",
        timestamp_buy=123455,
        price_buy="2.02",
        timestamp_sell=12345,
        price_sell="2.34"
    )
    addOrder(orderEntity)


from src.core.tradinglines.supportAndResistance import SupportResistance


def testSupportResistance():
    coin = coins.ATACoin()
    ma = MovingAverage(
        coin=coin,
        ma=[20, 100],
        interval="1h",
        limit=300
    )
    ma.setMovingAverage()
    sp = SupportResistance(movingAverage=ma)
    sp.set()
    print(sp.getSupportAndResistance())
    sp.createChart()


# from src.core.tradinglines.candleStickChart import CandleStickChart
#
# def testCandleStickChart():
#     coin = coins.ATACoin()
#     candleStickChart = CandleStickChart(
#         coin=coin,
#         ma=[15, 80],
#         interval="15m",
#         limit=10
#     )
#     candleStickChart.set()


if __name__ == "__main__":
    # testCheckTimeServer()
    # testAccountInformation()
    # testCandleStick()

    # extime = 1635400800000
    #
    # import datetime
    # import time
    # print(time.ctime(int(extime/1000)))
    # testMa20Ma501H()
    # testAlgo1()
    # testAlgo2()
    # testOrderBook()
    # testAssetInformation()
    # testNewOrder()
    # testQuantityForSell()
    # testQuantityForBuy()
    # testNewOCO()

    # testQueryOrder()
    # testAllOrder()
    # testCancelOrder()

    # asyncio.run(runner1.run())
    # testRunner2()

    # testMacd()
    # testAlgo3()
    testRunner3()

    # testAlgo4()

    # getOrders()
    # testOrderEntity()

    # testAlgo5()
    # testAddOrder()
    # testGetOrders()

    # testSupportResistance()
    # from main2 import run
    # run()

    # testCandleStickChart()
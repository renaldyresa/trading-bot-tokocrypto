from src.core.tradinglines.movingAverage import MovingAverage
from src.insfrastructures.api_requests.orderbook import OrderBook


class Algo2:
    """
    algo2 untuk mengetahui harga sekarang sedang berada di atas garis ma1 dan ma2
    """
    def __init__(self, ma: MovingAverage):
        self.ma = ma

    def isBuy(self):
        tails = self.ma.df.tail(1)
        nameMa1 = self.ma.generateColumnNameMA(self.ma.mAs[0])
        nameMa2 = self.ma.generateColumnNameMA(self.ma.mAs[1])
        # print(tails[nameMa2])

        orderBook = OrderBook()
        orderBook.setParams(
            symbol=self.ma.coin.toUSDT(),
            limit=10
        )
        response = orderBook.send()
        currentPrice = float(response["asks"][0][0])
        if currentPrice > float(tails[nameMa2]):
            return True
        return False
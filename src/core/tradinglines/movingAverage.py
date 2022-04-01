import matplotlib.pyplot as plt
from src.insfrastructures.api_requests.candlestick import CandleStick
from src.domains.bases.baseCoin import BaseCoin


class MovingAverage:

    def __init__(self, coin: BaseCoin, ma: list, interval="15m", limit=500):
        self.__coin = coin
        self.__ma = ma
        self.__interval = interval
        self.__limit = limit
        candlestick = CandleStick()
        candlestick.setParams(
            symbol=coin.toUSDT(False),
            interval=interval,
            limit=limit
        )
        self.title = f"TOKO CRYPTO : {coin.toUSDT(False)}-{interval}"
        self.df = candlestick.send()
        self.mAs = ma

    def generateColumnNameMA(self, numberMA):
        return f"MA for {numberMA} {self.__interval}"

    @property
    def interval(self):
        return self.__interval

    @property
    def coin(self):
        return self.__coin

    def clone(self):
        return MovingAverage(coin=self.__coin, ma=self.__ma, interval=self.__interval, limit=self.__limit)

    def setMovingAverage(self):
        for ma in self.mAs:
            columnName = self.generateColumnNameMA(ma)
            self.df[columnName] = self.df['close'].rolling(ma).mean()

    def createChart(self):
        plt.figure(figsize=(13, 4))
        plt.plot(self.df["close"], label="Closing Price")
        for ma in self.mAs:
            plt.plot(self.df[self.generateColumnNameMA(ma)], label=f"{ma} {self.__interval} Moving Average")
        plt.title(self.title)
        plt.legend()
        plt.show()

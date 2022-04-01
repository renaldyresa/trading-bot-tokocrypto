import pandas as pd
import matplotlib.pyplot as plt
from src.insfrastructures.api_requests.candlestick import CandleStick
from src.domains.bases.baseCoin import BaseCoin
from src.core.tradinglines.movingAverage import MovingAverage


class MACD:

    def __init__(self, coin: BaseCoin, interval="15m", limit=500):
        self.__coin = coin
        self.__interval = interval
        self.__limit = limit
        candlestick = CandleStick()
        candlestick.setParams(
            symbol=coin.toUSDT(False),
            interval=interval,
            limit=limit
        )
        self.df = candlestick.send()["close"]
        self.slow, self.fast,  self.smooth = 26, 12, 9
        self.dfResult: pd.DataFrame = None
        self.title = f"TOKO CRYPTO : {coin.toUSDT(False)}-{interval}"

    @property
    def coin(self):
        return self.__coin

    def setMACD(self):
        df = self.df.copy()
        exp1 = df.ewm(span=self.fast, adjust=False).mean()
        exp2 = df.ewm(span=self.slow, adjust=False).mean()
        macd = pd.DataFrame(exp1 - exp2).rename(columns={'close': 'macd'})
        signal = pd.DataFrame(macd.ewm(span=self.smooth, adjust=False).mean()).rename(columns={'macd': 'signal'})
        hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns={0: 'hist'})
        frames = [macd, signal, hist]
        self.dfResult = pd.concat(frames, join='inner', axis=1)
        # print(self.dfResult.tail(10))

    def createChart(self, movingAverage: MovingAverage=None):
        prices, hist = self.df, self.dfResult['hist']

        ax1 = plt.subplot2grid((8, 1), (0, 0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((8, 1), (5, 0), rowspan=3, colspan=1)

        ax1.plot(prices)
        ax2.plot(self.dfResult['macd'], color='grey', linewidth=1.5, label='MACD')
        ax2.plot(self.dfResult['signal'], color='skyblue', linewidth=1.5, label='SIGNAL')
        if movingAverage is not None:
            for ma in movingAverage.mAs:
                ax1.plot(movingAverage.df[movingAverage.generateColumnNameMA(ma)], label=f"{ma} {self.__interval} Moving Average")

        for i in range(len(prices)):
            if str(hist[i])[0] == '-':
                ax2.bar(prices.index[i], hist[i], color='#ef5350')
            else:
                ax2.bar(prices.index[i], hist[i], color='#26a69a')

        plt.title(self.title)
        plt.show()


from src.core.tradinglines.movingAverage import MovingAverage
from src.domains.bases.baseCoin import BaseCoin


class Algo4:
    """
    algo4 untuk mengetahui ketika tred lagi bullish
    """

    def __init__(self, coin: BaseCoin):
        self.moveAverage = MovingAverage(
            coin=coin,
            ma=[30, 100],
            interval="1d",
            limit=500
        )
        self.moveAverage.setMovingAverage()

    #todo algoritma ketika tred sedang bullish
    def isBuy(self):
        # self.moveAverage.createChart()
        nameMa1 = self.moveAverage.generateColumnNameMA(self.moveAverage.mAs[0])
        nameMa2 = self.moveAverage.generateColumnNameMA(self.moveAverage.mAs[1])
        rows = self.moveAverage.df.tail(40)
        for row in rows:
            if float(row[nameMa1]) < float(row[nameMa2]):
                return False
        return True
        # if lastRow['close']
        # print(self.moveAverage.df['volume'])
        # return True
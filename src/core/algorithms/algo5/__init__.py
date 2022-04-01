from src.core.tradinglines.movingAverage import MovingAverage
from src.insfrastructures.api_requests.candlestick import CandleStick
from src.domains.bases.baseCoin import BaseCoin


class Algo5:

    def __init__(self, coin: BaseCoin):
        self.coin = coin
        self.candlestick = CandleStick()
        self.candlestick.setParams(
            symbol=coin.toUSDT(False),
            interval="30m",
            limit=10
        )

    def isBuy(self):
        response = self.candlestick.send()
        lastRow = response.iloc[-2]
        lastTRow = response.iloc[-3]
        high = float(lastRow['high'])
        low = float(lastRow['low'])
        close = float(lastRow['close'])
        tHigh, tLow, tClose = float(lastTRow['high']), float(lastTRow['close']), float(lastTRow['close'])
        # print(high, low, close)
        ak1 = high-low
        ak2 = high-close
        result1 = ak2/ak1 < 0.3
        # tak1 = tHigh-tLow
        # tak2 = tHigh-tClose
        # result2 = tak2/tak1 < 0.5
        if result1:
            return True
        return False




import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpl_dates
from src.insfrastructures.api_requests.candlestick import CandleStick
from src.domains.bases.baseCoin import BaseCoin


class CandleStickChart:

    def __init__(self, coin: BaseCoin, ma: list, interval="15m", limit=200):
        self.__listMa = ma
        self.__coin = coin
        self.__interval = interval
        self.__limit = limit
        dataChart = CandleStick()
        dataChart.setParams(
            symbol=coin.toUSDT(False),
            interval=interval,
            limit=limit
        )
        self.title = f"TOKO CRYPTO : {coin.toUSDT(False)}-{interval}"
        self.df = dataChart.send()
        self.df.rename(
            columns={
                'close time': 'Date',
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close'
            }, inplace=True)

    def set(self):
        plt.style.use('ggplot')
        ohlc = self.df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
        ohlc['Date'] = pd.to_datetime(ohlc['Date'])
        ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
        ohlc = ohlc.astype(float)

        fig, ax = plt.subplots()

        candlestick_ohlc(ax, ohlc.values, width=0.1, colorup='green', colordown='red', alpha=0.8)
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        fig.suptitle("Chart Candle Stick")

        # Formatting Date
        # date_format = mpl_dates.Date('%d-%m-%Y %h:%m:%s')
        # ax.xaxis.set_major_formatter(date_format)
        # fig.autofmt_xdate()

        fig.tight_layout()

        plt.show()



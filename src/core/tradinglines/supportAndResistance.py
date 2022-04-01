import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# from mplfinance import candlestick_ohlc
from src.core.tradinglines.movingAverage import MovingAverage


class SupportResistance:

    def __init__(self, movingAverage: MovingAverage):
        self.__movingAverage = movingAverage
        self.__s = np.mean(self.__movingAverage.df["high"] - self.__movingAverage.df["low"])
        self.__levels = []

    def isSupport(self, i):
        support = self.__movingAverage.df['low'][i] < self.__movingAverage.df['low'][i - 1] < \
                  self.__movingAverage.df['low'][i - 2] \
                  and self.__movingAverage.df['low'][i] < self.__movingAverage.df['low'][i + 1] < \
                  self.__movingAverage.df['low'][i + 2]
        return support

    def isResistance(self, i):
        resistance = self.__movingAverage.df['high'][i] > self.__movingAverage.df['high'][i - 1] > \
                     self.__movingAverage.df['high'][i - 2] \
                     and self.__movingAverage.df['high'][i] > self.__movingAverage.df['high'][i + 1] > \
                     self.__movingAverage.df['high'][i + 2]
        return resistance

    def isFarFromLevel(self, l):
        return np.sum([abs(l-x) < self.__s for x in self.__levels]) == 0

    def set(self):
        for i in range(2, self.__movingAverage.df.shape[0]-2):
            if self.isSupport(i):
                l = self.__movingAverage.df["low"][i]
                if self.isFarFromLevel(l):
                    self.__levels.append((i, l))
            elif self.isResistance(i):
                l = self.__movingAverage.df["high"][i]
                if self.isFarFromLevel(l):
                    self.__levels.append((i, l))

    def getSupportAndResistance(self):
        lastRow = self.__movingAverage.df.iloc[-1]
        priceClose = float(lastRow["close"])
        support, resistance = self.__levels[0][1], self.__levels[0][1]
        for level in self.__levels:
            if support - priceClose > level[1] - priceClose > 0:
                support = level[1]
            if resistance - priceClose > priceClose - level[1] > 0:
                resistance = level[1]
        return support, resistance, priceClose

    def createChart(self):
        plt.figure(figsize=(13, 4))
        plt.plot(self.__movingAverage.df["close"], label="closing price")
        for ma in self.__movingAverage.mAs:
            plt.plot(self.__movingAverage.df[self.__movingAverage.generateColumnNameMA(ma)],
                     label=f"{ma} {self.__movingAverage.interval} Moving Average")
        for level in self.__levels:
            plt.hlines(y=level[1], xmin=level[0], xmax=self.__movingAverage.df.shape[0], colors="purple")
        plt.title(self.__movingAverage.title)
        # plt.legend()
        plt.show()



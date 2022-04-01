import math
import pandas as pd
from src.core.tradinglines.macd import MACD
from sklearn import preprocessing
from src.insfrastructures.api_requests.orderbook import OrderBook


class Algo3:
    """
    algo3 manggunakan macd untuk mengetahui saat beli, saat bar merah ke bar hijau
    """

    def __init__(self, macd: MACD):
        self.macd = macd

    def isBuy(self):
        # print(self.macd.dfResult.head())
        x = self.macd.dfResult.values  # returns a numpy array

        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        df = pd.DataFrame(x_scaled)
        # print(df.tail(10))
        tails = self.macd.dfResult.tail(10)
        lastRow = df.tail(1)
        results = []
        for _, row in tails.iterrows():
            results.append(float(row[1]) > float(row[0]))
        if results.count(True) > results.count(False) and 0.2 > float(lastRow[1])-float(lastRow[0]) > -0.25:
            return True
        return False
        # lastRow = self.macd.dfResult.tail(1)
        # tails = self.macd.dfResult.tail(5)
        # tRow = self.macd.dfResult.iloc[-6]
        # results = []
        # # for _, row in tails.iterrows():
        # #     results.append(tRow['hist'] < row['hist'])
        # #     print(row)
        # #     tRow = row
        # hist = float(lastRow['hist'])
        # fact, whole = math.modf(hist)
        # strFact = str(fact)
        # if 0.3 > (whole+fact*(len(strFact)*10)) > -0.5:
        #     return True
        # return False
        # print(tails)




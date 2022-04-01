import time
import pandas as pd


def candleToPandas(data: list) -> pd.DataFrame:
    dataFrame = pd.DataFrame(
        data=data,
        columns=("open time", "open", "high", "low",
                 "close", "volume", "close time", "quote asset volume",
                 "number of trades", "taker buy base", "taker buy quote",
                 "ignore")
    )
    # print(dataFrame["quote asset volume"])
    deleteColumns = ["quote asset volume", "number of trades",
                     "taker buy base", "taker buy quote", "ignore"]
    dataFrame = dataFrame.drop(columns=deleteColumns, axis=1)
    dataFrame['close time'] = dataFrame['close time'].apply(lambda x: time.ctime(int(int(x)/1000)))
    # dataFrame['open time'] = dataFrame['open time'].apply(lambda x: time.ctime(int(int(x)/1000)))
    dataFrame["close"] = dataFrame.close.astype(float)
    dataFrame["high"] = dataFrame.high.astype(float)
    dataFrame["low"] = dataFrame.low.astype(float)
    return dataFrame

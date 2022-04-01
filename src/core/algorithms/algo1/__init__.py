from src.core.tradinglines.movingAverage import MovingAverage


class Algo1:
    """
    algo 1 untuk mengetahui ketika garis ma saling silang
    """

    def __init__(self, ma: MovingAverage):
        self.ma = ma

    def isBuy(self):
        nameMa1 = self.ma.generateColumnNameMA(self.ma.mAs[0])
        nameMa2 = self.ma.generateColumnNameMA(self.ma.mAs[1])
        closeMA1 = self.ma.df.iloc[-1][nameMa1]
        closeMA2 = self.ma.df.iloc[-1][nameMa2]
        diffMA = closeMA2-closeMA1
        calculateToleranceError = (diffMA/(closeMA2+closeMA1))*100
        # print(calculateToleranceError)
        result = -0.7 < calculateToleranceError < 0.7
        volume = float(self.ma.df.iloc[-1]["volume"]) > 400000
        return result and volume

class BaseCoin:

    def __init__(self, symbol: str):
        self.__symbol = symbol

    @property
    def symbol(self):
        return self.__symbol

    def toUSDT(self, withUnderLine=True):
        if withUnderLine:
            return f"{self.__symbol}_USDT"
        return f"{self.__symbol}USDT"

    def toBIDR(self, withUnderLine=True):
        if withUnderLine:
            return f"{self.__symbol}_BIDR"
        return f"{self.__symbol}BIDR"
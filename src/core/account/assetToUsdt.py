from src.insfrastructures.api_requests.assetInformation import AssetInformation
from src.insfrastructures.api_requests.accountInformation import AccountInformation
from src.insfrastructures.api_requests.queryOrder import QueryOrder
from src.insfrastructures.api_requests.allOrder import AllOrder


class AssetToUSDT:

    def __init__(self):
        self.__assets = []

    def __getAllAsset(self):
        accountInformation = AccountInformation()
        accountInformation.setParams()
        accountInformation.setSignature()
        response = accountInformation.send()
        assets = response["data"]["accountAssets"]
        ignoreCoins = ["USDT", "BIDR"]
        for asset in assets:
            if float(asset["free"]) > 1.0 and asset["asset"] not in ignoreCoins:
                self.__assets.append(asset)

    def run(self):
        self.__getAllAsset()
        for asset in self.__assets:
            allOrder = AllOrder()
            allOrder.setParams(
                symbol=asset["asset"]
            )




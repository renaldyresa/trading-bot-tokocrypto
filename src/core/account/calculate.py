from src.domains.bases.baseCoin import BaseCoin
from src.insfrastructures.api_requests.orderbook import OrderBook
from src.insfrastructures.api_requests.assetInformation import AssetInformation


def getQuantityAndOrderBookForSell(coin: BaseCoin, percentWallet=50, limit=10):
    assetInformation = AssetInformation()
    assetInformation.setParams(
        asset=coin.symbol,
    )
    orderBook = OrderBook()
    orderBook.setParams(
        symbol=coin.toUSDT(),
        limit=limit,
    )
    res = orderBook.send()
    assetInformation.setSignature()
    totalAsset = assetInformation.send()
    return str(int(float(totalAsset))), res


def getQuantityAndOrderBookForBuy(coin: BaseCoin, percentWallet=50, limit=10):
    usdtAsset = AssetInformation()
    usdtAsset.setParams(
        asset="USDT"
    )
    usdtAsset.setSignature()
    totalUsdt = usdtAsset.send()

    orderBook = OrderBook()
    orderBook.setParams(
        symbol=coin.toUSDT(),
        limit=limit,
    )
    res = orderBook.send()
    price = res["asks"][0][0]
    quantity = int(float(totalUsdt)/float(price))*(percentWallet/100)
    return f"{int(quantity)}", res

# -*- encoding: utf8 -*-
# © Toons

import json
import requests
# import sys, imp, traceback
# from .. import setInterval


def getTokenPrice(token, fiat="usd"):
    cmc_ark = json.loads(requests.get("https://api.coinmarketcap.com/v1/ticker/"+token+"/?convert="+fiat).text)
    try:
        return float(cmc_ark[0]["price_%s" % fiat])
    except requests.ConnectionError:
        return 1


def getArkFiatPrice(fiat):
    """
    Allow to get the current price of Ark in one of the major currency
    :param fiat: The currency we wants to convert
    :return: The price in the specified currency
    """
    fiats = ["usd", "eur", "chf", "aud", "gbp", "jpy"]
    if fiat in fiats:
        r = json.loads(requests.get("https://api.coinmarketcap.com/v1/ticker/ark/?convert=%s" % fiat).text)
        return r[0]["price_%s" % fiat][0:7]
    raise AttributeError("Currency not found")
    # return 1


def getArkPriceFromCryptoCompare(currency):
    """
    Allow to get the current price of Ark converted in any fiat or cryptocurrency existing on Cryptocompare.
    Use like : getArkPriceFromCryptoCompare("usd") or getArkPriceFromCryptoCompare("dash")
    """
    base_url = "https://min-api.cryptocompare.com/data/price?fsym=ARK&tsyms=%s" % currency.upper()
    fiats = ["usd", "eur", "chf", "aud", "gbp", "jpy"]
    coins = getAllCoinsFromCryptoCompare()
    if currency in fiats or currency.upper() in coins:
        currency = currency.upper()
        r = json.loads(requests.get(base_url).text)
        return r[currency]
    raise AttributeError("Currency not found")
    # return 1


def getArkPriceFromCryptoCompareBis(*args):
    """
    Allow to get the current price of Ark converted in any fiat or cryptocurrency existing on Cryptocompare with the
    possibility of fetching the price for multiples currencies at the same time.

    At the moment it works but it's probably not the most optimal way to do it.
    Should have a better name to represent what it does.

    Use like : getArkPriceFromCryptoCompareBis("usd", "chf", "eur", "btc"))

    :param args: The currency/(ies) we wants to convert
    :return: The price(s) we wants as a python dict
    """
    url = "https://min-api.cryptocompare.com/data/price?fsym=ARK&tsyms="
    try:
        for currency in args:
            url += currency.upper() + ','
        r = json.loads(requests.get(url[:-1]).text)
        return r
    except requests.ConnectionError:
        return 1


def getAllCoinsFromCryptoCompare():
    """
    Retrieve of all of the coins acronyms on CryptoCompare
    """
    try:
        r = json.loads(requests.get("https://www.cryptocompare.com/api/data/coinlist/").text)
        coins = []
        for coin in r["Data"]:
            coins.append(coin)
        return coins
    except requests.ConnectionError:
        return 1


def getArkPriceFromBittrex():
    """
    Get the last price of Ark on Bittrex. The showed price is in Bitcoin.
    """
    try:
        r = json.loads(requests.get("https://bittrex.com/api/v1.1/public/getmarketsummary?market=btc-ark").text)
        return r["result"][0]["Last"]
    except requests.ConnectionError:
        return 1


def getArkPriceFromCryptopia():
    """
    Get the last price of Ark on Cryptopia. The showed price is in Bitcoin.
    """
    try:
        r = json.loads(requests.get("https://www.cryptopia.co.nz/api/GetMarket/ARK_BTC").text)
        return r["Data"]["LastPrice"]
    except requests.ConnectionError:
        return 1


def getArkPriceFromLitebit():
    """
    Get the last (selling) price of Ark on Litebit. The showed price is in USD.
    """
    try:
        r = json.loads(requests.get("https://api.litebit.eu/market/ark").text)
        return r["result"]["buy"]
    except requests.ConnectionError:
        return 1


def getArkPriceFromCryptomate():
    """
    Get the current price on Cryptomate. The showed price is in USD.
    """
    try:
        r = json.loads(requests.get("https://cryptomate.co.uk/api/ark/").text)
        return r["ARK"]["price"]
    except requests.ConnectionError:
        return 1


# def getTokenPrice(token, fiat="usd"):
# 	cmc_ark = json.loads(requests.get("http://coinmarketcap.northpole.ro/api/v5/%s.json" % token).text)
# 	return float(cmc_ark["price"][fiat])

# class ExchangeNoImplemented(Exception): pass
# class ExchangeApiError(Exception): pass

# def main_is_frozen():
# 	return (hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__"))

# class Exchange:

# 	frozen_mode = False

# 	@staticmethod
# 	def _printError(error):
# 		if hasattr(error, "__traceback__"):
# 			sys.stdout.write("".join(traceback.format_tb(error.__traceback__)).rstrip() + "\n")
# 		sys.stdout.write("%s\n" % error)

# 	@staticmethod
# 	def coinmarketcap(curency):
# 		try:
# 			cmc_ark = json.loads(requests.get("http://coinmarketcap.northpole.ro/api/v5/ARK.json").text)
# 			return float(cmc_ark["price"][curency])
# 		except Exception as error:
# 			Exchange._printError(error)

# 	@staticmethod
# 	def cryptocompare(curency):
# 		try:
# 			if Exchange.frozen_mode:
# 				ccp_ark = json.loads(requests.get("https://min-api.cryptocompare.com/data/price?fsym=ARK&tsyms=USD,EUR,GBP,CNY", verify='cacert.pem').text)
# 			else:
# 				ccp_ark = json.loads(requests.get("https://min-api.cryptocompare.com/data/price?fsym=ARK&tsyms=USD,EUR,GBP,CNY").text)
# 			return float(ccp_ark[curency.upper()])
# 		except Exception as error:
# 			Exchange._printError(error)

# def useExchange(name):
# 	Exchange.frozen_mode = main_is_frozen()
# 	global getArkPrice
# 	try: getArkPrice = getattr(Exchange, name)
# 	except: raise ExchangeNoImplemented("%s exchange not implemented yet" % name.capitalize())
# 	else: return name.capitalize()

# useExchange("coinmarketcap")

# def getKrakenPair(pair):
# 	data = json.loads(requests.get("https://api.kraken.com/0/public/Ticker?pair="+pair.upper()).text)
# 	A, B = pair[:3], pair[3:]
# 	A = ("Z" if A in ['USD', 'EUR', 'CAD', 'GPB', 'JPY'] else "X") + A
# 	B = ("Z" if B in ['USD', 'EUR', 'CAD', 'GPB', 'JPY'] else "X") + B
# 	try: return float(data["result"][A + B]["c"][0])
# 	except: return -1


# def getPoloniexPair(pair):
# 	if "_" not in pair: pair = pair[:3] + "_" + pair[3:]
# 	return float(poloniex_json[pair]["last"])

# # poloniex global data 
# # reload data every 30 seconds
# @setInterval(60) 
# def load():
# 	global poloniex_json
# 	poloniex_json = json.loads(requests.get("https://poloniex.com/public?command=returnTicker").text)
# # load()

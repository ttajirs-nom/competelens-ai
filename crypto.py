import os
import requests
from dotenv import load_dotenv

load_dotenv()

CMC_API_KEY = os.getenv("COINMARKETCAP_API_KEY")
COINS = ["BTC", "ETH", "SOL"]


def get_crypto_prices():
    """
    CoinMarketCap free API se BTC, ETH, SOL prices + BTC Dominance nikaalta hai.
    """
    prices = []
    try:
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
        params = {"symbol": ",".join(COINS), "convert": "USD"}

        response = requests.get(url, headers=headers, params=params, timeout=8)
        data = response.json()

        for symbol in COINS:
            coin_data = data.get("data", {}).get(symbol)
            if coin_data:
                if isinstance(coin_data, list):
                    coin_data = coin_data[0]
                price = coin_data["quote"]["USD"]["price"]
                prices.append({"symbol": symbol, "price": price})

        # BTC Dominance (USDT.D ka free-tier equivalent nahi milta, BTC.D standard hai)
        dom_url = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest"
        dom_response = requests.get(dom_url, headers=headers, timeout=8)
        dom_data = dom_response.json()
        btc_dominance = dom_data.get("data", {}).get("btc_dominance")
        if btc_dominance is not None:
            prices.append({"symbol": "BTC.D", "price": btc_dominance, "is_percent": True})

    except Exception as e:
        print(f"Crypto fetch error: {e}")

    return prices
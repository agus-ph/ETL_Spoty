from pycoingecko import CoinGeckoAPI
from datetime import datetime
import pandas as pd

# ------------------ Extracting data to feed the dashboard --------------------

# We'll use pycoingecko module from https://github.com/man-c/pycoingecko to extract data

cg = CoinGeckoAPI()

# Next list contains de crypto ids (you can find it on coingecko) of our interest

coin_list = [
    "bitcoin",
    "ethereum",
    "litecoin",
    "cardano",
    "dogecoin",
    "ripple",
    "monero",
    "binancecoin",
    "stellar",
]


def generate_crypto_historic(crypto):
    """
    This function extract te historical data of a crypto (last 365 days, in usd)
    """
    crypto_historic = cg.get_coin_market_chart_by_id(crypto, "usd", 365)

    return crypto_historic


def generate_crypto_df(crypto_historic, crypto):
    """
    This function takes the historical data and transform it in a useful dataframe
    """
    df = pd.DataFrame(crypto_historic)
    df_price = pd.DataFrame(df["prices"].to_list(), columns=["date", "prices"])
    df_mc = pd.DataFrame(df["market_caps"].to_list(), columns=["date2", "market_caps"])
    df_tv = pd.DataFrame(
        df["total_volumes"].to_list(), columns=["date3", "total_volumes"]
    )
    df_join = df_price.join([df_mc, df_tv])
    df_join["name"] = crypto
    crypto_df = df_join.loc[
        :, ["date", "name", "prices", "market_caps", "total_volumes"]
    ]
    crypto_df["date"] = pd.to_datetime(crypto_df["date"], unit="ms", origin="unix")
    crypto_df["date"] = crypto_df["date"].dt.strftime("%d-%m-%Y")

    return crypto_df


df_list = []

for currencie in coin_list:
    crypto_historic = generate_crypto_historic(currencie)
    cripto_df = generate_crypto_df(crypto_historic, currencie)
    df_list.append(cripto_df)

final_df = pd.concat(df_list)


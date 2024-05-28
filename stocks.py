import requests
import pandas as pd
from typing import List, Dict

from config import REQUEST_HEADERS


def _get_stocks_by_exchange(exchange: str, us_only: bool = True) -> List[Dict]:
    return requests.get(
        f'https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=4000&exchange={exchange}' + us_only * '&country=united_states',
        headers=REQUEST_HEADERS
    ).json()['data']['table']['rows']

def get_stocks(nyse: bool = True, nasdaq: bool = True) -> pd.DataFrame:
    stocks = []

    if nyse:
        stocks.extend(_get_stocks_by_exchange('nyse'))
    if nasdaq:
        stocks.extend(_get_stocks_by_exchange('nasdaq'))

    stocks = pd.DataFrame(data=stocks)

    stocks = stocks[(stocks['marketCap'] != 'NA')]
    stocks['symbol'] = stocks['symbol'].str.replace('/', '-')
    stocks['lastsale'] = stocks['lastsale'].str.replace('\$|,', '', regex=True).astype('float64')
    stocks['marketCap'] = stocks['marketCap'].str.replace(',', '').astype('int64')

    return stocks[['symbol', 'name', 'lastsale', 'marketCap']].sort_values('marketCap', ascending=False).reset_index(drop=True)
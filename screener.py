from tradingview_screener import Query, Column
from datetime import datetime, time
from yfinance import Ticker
from time import sleep
import winsound

from utils import get_current_session

    
BASE_FILTER = [
    Column('type') == 'stock',
    Column('is_primary') == True,
    Column('exchange').isin(['NASDAQ', 'NYSE']),
]

QUERIES = {
    'DAY_LONG_MOMENTUM_QUERY':
        Query().
        select('close', 'change|5', 'change_abs|5', 'market_cap_basic', 'Value.Traded|5', 'sector').
        where(
            *BASE_FILTER,
            Column('change|5') > 1,
            Column('Value.Traded|5') > 0.5e6,
            Column('market_cap_basic') > 30e6
        ).
        order_by('change|5', ascending=False),
    'DAY_SHORT_MOMENTUM_QUERY':
        Query().
        select('close', 'change|5', 'market_cap_basic', 'Value.Traded|5', 'sector').
        where(
            *BASE_FILTER,
            Column('change|5') < -1,
            Column('Value.Traded|5') > 0.5e6,
            Column('market_cap_basic') > 30e6
        ).
        order_by('change|5', ascending=True),
    'PRE_LONG_MOMENTUM_QUERY':
        Query().
        select('close', 'volume', 'market_cap_basic', 'premarket_change').
        where(
            *BASE_FILTER,
            Column('premarket_change') > 3,
            Column('market_cap_basic') > 30e6
        ).
        order_by('premarket_change', ascending=False)
}


class Screener:
    
    def scan(self):
        while True:
            match get_current_session():
                case 'MAIN':
                    self._scan_main()
                case 'PRE-MARKET':
                    self._scan_pre()
                
    def _scan_main(self):
        return
    
    def _scan_pre(self):
        n, init_df = QUERIES['PRE_LONG_MOMENTUM_QUERY'].get_scanner_data()
        tickers = init_df.ticker.to_list()
        for i, row in init_df.iterrows():
            print(f'================== {row.ticker} - {row.premarket_change :.2f}% ==================')
            for news in self.find_news(row.ticker):
                print(f'[{news["providerPublishTime"]}]', news['title'])
            print()

        while get_current_session() == 'PRE-MARKET':

            n, df = QUERIES['PRE_LONG_MOMENTUM_QUERY'].get_scanner_data()

            for i, row in df.iterrows():
                if row.ticker in tickers:
                    # what if it's surging even more with a new catalyst?
                    continue
                tickers.append(row.ticker)
                winsound.Beep(3400, 500)
                print(f'================== {row.ticker} - {row.premarket_change :.2f}% ==================')
                for news in self.find_news(row.ticker):
                    print(f'[{news["providerPublishTime"]}]', news['title'])
                print()
                
            sleep(10)

    def find_news(self, ticker: str, starting_from: datetime = datetime.combine(datetime.today(), time.min)):
        news = []
        yf_ticker = Ticker(ticker)
        for n in yf_ticker.get_news():
            dt = datetime.fromtimestamp(n['providerPublishTime'])
            if dt > starting_from:
                n['providerPublishTime'] = dt
                news.append(n)
        return news
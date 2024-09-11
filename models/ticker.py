import yfinance
from pandas import Series
from datetime import datetime
from edgar import Company, set_identity
from finvizfinance.quote import finvizfinance

from models.enums import SessionEnum
from utils import asyncify

set_identity('Hlib Sin sinixyowo@gmail.com')


class Ticker:
    def __init__(self, symbol: str, company: str, sector: str, session: str, technicals: dict = {}):
        self.symbol = symbol
        self.company = company
        self.sector = sector
        self.session = session

        self.technicals = technicals

    @staticmethod
    def from_pandas(series: Series, session: str):
        technicals = {'market_cap': series['market_cap_basic'], 'close': series['close']}
        match session:
            case SessionEnum.PRE_MARKET:
                technicals.update({
                    'session_change': series['premarket_change'],
                    'session_volume': series['premarket_volume'],
                    'session_close': series['premarket_close'],
                    'session_value': series['premarket_value']
                })
            case SessionEnum.DAY:
                technicals.update({
                    'session_change': series['change|5'],
                    'session_value': series['Value.Traded|5'],
                    'session_close': series['close']
                })
            case SessionEnum.POST_MARKET:
                technicals.update({
                    'session_change': series['postmarket_change'],
                    'session_volume': series['postmarket_volume'],
                    'session_close': series['postmarket_close'],
                    'session_value': series['postmarket_value']
                })
        return Ticker(series['ticker'], series['description'], series['sector'], session, technicals=technicals)

    @asyncify
    def find_news(self, starting_from: datetime = datetime.combine(datetime.today(), datetime.min.time())):
        news = []
        yf_ticker = yfinance.Ticker(self.symbol)
        for n in yf_ticker.get_news():
            dt = datetime.fromtimestamp(n['providerPublishTime'])
            if dt > starting_from:
                n['providerPublishTime'] = dt
                news.append(n)
        return news
    
    @asyncify
    def get_filings(self):
        company = Company(self.symbol)
        if company:
            return company.get_filings()
        else:
            None

    @asyncify
    def get_full_technicals(self):
        return finvizfinance(self.symbol).ticker_fundament()
from tradingview_screener import Query
import pandas as pd
import asyncio

from utils import get_current_session, asyncify
from models.enums import SessionEnum, QueryEnum
from models.ticker import Ticker
from bot.report import report


class Screener:

    def __init__(self):
        self._hot_tickers = []
        self.__is_initial_scan = True

    async def scan(self):
        while True:
            self._hot_tickers.clear()
            match get_current_session():
                case SessionEnum.DAY:
                    await self._scan_day()
                case SessionEnum.PRE_MARKET:
                    await self._scan_pre()
                case SessionEnum.POST_MARKET:
                    await self._scan_post()
                case SessionEnum.CLOSED:
                    await asyncio.sleep(5)

    async def _scan_pre(self):
        while get_current_session() == SessionEnum.PRE_MARKET:
            df = await self.__get_pre_screener_state()
            await self.__scan_session(df, SessionEnum.PRE_MARKET)
            await asyncio.sleep(10)

    async def _scan_day(self):
        while get_current_session() == SessionEnum.DAY:
            df = await self.__get_day_screener_state()
            await self.__scan_session(df, SessionEnum.DAY)
            await asyncio.sleep(10)
    
    async def _scan_post(self):
        while get_current_session() == SessionEnum.POST_MARKET:
            df = await self.__get_post_screener_state()
            await self.__scan_session(df, SessionEnum.POST_MARKET)
            await asyncio.sleep(10)

    async def __scan_session(self, scanner_state: pd.DataFrame, session: str):
        for _, row in scanner_state.iterrows():
            ticker = Ticker.from_pandas(row, session)
            if ticker.symbol in self._hot_tickers:
                continue
            self._hot_tickers.append(ticker.symbol)
            asyncio.create_task(report(ticker, self.__is_initial_scan))
        self.__is_initial_scan = False

    async def __get_pre_screener_state(self) -> pd.DataFrame:
        gainers = await Screener.exec_query(QueryEnum.PRE_LONG_MOMENTUM)
        losers = await Screener.exec_query(QueryEnum.PRE_SHORT_MOMENTUM)
        df = pd.concat([gainers, losers])
        if len(df) > 0:
            df['premarket_value'] = df.eval('close / 2 * premarket_volume')
            df = df[df['premarket_value'] > 5e5]
        return df

    async def __get_day_screener_state(self) -> pd.DataFrame:
        gainers = await Screener.exec_query(QueryEnum.DAY_LONG_MOMENTUM)
        losers = await Screener.exec_query(QueryEnum.DAY_SHORT_MOMENTUM)
        df = pd.concat([gainers, losers])
        return df

    async def __get_post_screener_state(self) -> pd.DataFrame:
        gainers = await Screener.exec_query(QueryEnum.POST_LONG_MOMENTUM)
        losers = await Screener.exec_query(QueryEnum.POST_SHORT_MOMENTUM)
        df = pd.concat([gainers, losers])
        if len(df) > 0:
            df['postmarket_value'] = df.eval('close / 2 * postmarket_volume')
            df = df[df['postmarket_value'] > 5e5]
        return df

    @staticmethod
    def exec_query_sync(query: Query) -> pd.DataFrame:
        _, df = query.get_scanner_data()
        df['ticker'] = df.ticker.str.split(':').apply(lambda x: x[-1])
        return df

    @staticmethod
    @asyncify
    def exec_query(query: Query) -> pd.DataFrame:
        return Screener.exec_query_sync(query)

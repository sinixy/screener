from bot import bot
from db import db
from utils import stringify_mc
from models.ticker import Ticker


async def report(ticker: Ticker, is_initial_scan: bool = False):
    filing_section = ''
    if filings := await ticker.get_filings():
        recent_filing = filings[0]
        filing_section = f'📅 Latest Filing: <a href="{recent_filing.homepage_url}">{recent_filing.filing_date.isoformat()}</a>\n\n' \

    news_section = ''
    if news_list := await ticker.find_news():
        news_section = '📢 <b>News</b>\n'
        for news in news_list:
            news_section += f'[<a href="{news["link"]}">Link</a>][{news["providerPublishTime"].isoformat(sep=" ", timespec="minutes")}] {news["title"]}\n'

    technical_section = f'Market Cap: {stringify_mc(ticker.technicals["market_cap"])}\n'
    if technicals := await ticker.get_full_technicals():
        technical_section += f'Short Float: {technicals["Short Float"]}\n' \
                             f'Shs out/float: {technicals["Shs Outstand"]} | {technicals["Shs Float"]}\n' \
                             f'ATR: {technicals["ATR (14)"]}\n'
    technical_section += '\n'

    text = f'<b>{ticker.symbol} {ticker.technicals["session_change"] :.2f}%</b>\n\n' \
           f'Company: {ticker.company}\n' \
           f'Sector: {ticker.sector}\n\n' \
           + technical_section + filing_section + news_section
    
    for user in db.get_users():
        if user[1] == 0 and is_initial_scan: continue
        await bot.send_message(
            user[0],
            text,
            disable_web_page_preview=True
        )
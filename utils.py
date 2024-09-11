from datetime import datetime, time
import asyncio

from config import NY_TIMEZONE
from models.enums import SessionEnum


def get_current_session():
    now = datetime.now(tz=NY_TIMEZONE)
    tnow = now.time()
    weekday = now.weekday()
    
    if weekday in [5, 6]:
        return SessionEnum.CLOSED
    
    if time(9, 30) <= tnow < time(16, 0):
        return SessionEnum.DAY
    elif time(4, 0) <= tnow < time(9, 30):
        return SessionEnum.PRE_MARKET
    elif time(16, 0) <= tnow < time(20, 0):
        return SessionEnum.POST_MARKET
    else:
        return SessionEnum.CLOSED
    
def asyncify(f):
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: f(*args, **kwargs))
    return wrapper

def stringify_mc(market_cap):
    if market_cap > 1e12:
        return f'{market_cap / 1e12:.2f}T'
    elif market_cap > 1e9:
        return f'{market_cap / 1e9:.2f}B'
    elif market_cap > 1e6:
        return f'{market_cap / 1e6:.2f}M'
    else:
        return f'{market_cap / 1e3:.2f}K'
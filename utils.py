from datetime import datetime, time

from config import NY_TIMEZONE


def get_current_session():
    now = datetime.now(tz=NY_TIMEZONE)
    tnow = now.time()
    weekday = now.weekday()
    
    if weekday in [5, 6]:
        return 'CLOSED'
    
    if time(9, 30) <= tnow < time(16, 0):
        return 'MAIN'
    elif time(4, 0) <= tnow < time(9, 30):
        return 'PRE-MARKET'
    elif time(16, 0) <= tnow < time(20, 0):
        return 'POST-MARKET'
    else:
        return 'CLOSED'
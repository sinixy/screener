from tradingview_screener import Query, Column


class SessionEnum:
    PRE_MARKET = 'PRE-MARKET'
    DAY = 'DAY'
    POST_MARKET = 'POST-MARKET'
    CLOSED = 'CLOSED'

class RoleEnum:
    USER = 0
    ADMIN = 1

class QueryEnum:

    BASE_FILTER = [
        Column('type') == 'stock',
        Column('is_primary') == True,
        Column('exchange').isin(['NASDAQ', 'NYSE']),
    ]

    DAY_LONG_MOMENTUM = Query(). \
        select('description', 'sector', 'close', 'change|5', 'market_cap_basic', 'Value.Traded|5'). \
        where(
            *BASE_FILTER,
            Column('change|5').above_pct('ATRP', 1),
            Column('Value.Traded|5') > 5e5,
            Column('market_cap_basic') > 20e6
        ). \
        order_by('change|5', ascending=False)
    
    DAY_SHORT_MOMENTUM = Query(). \
        select('description', 'sector', 'close', 'change|5', 'market_cap_basic', 'Value.Traded|5'). \
        where(
            *BASE_FILTER,
            Column('change|5').below_pct('ATRP', -1),
            Column('Value.Traded|5') > 5e5,
            Column('market_cap_basic') > 20e6
        ). \
        order_by('change|5', ascending=True)
    
    PRE_LONG_MOMENTUM = Query(). \
        select('description', 'sector', 'close', 'premarket_volume', 'market_cap_basic', 'premarket_change', 'premarket_close'). \
        where(
            *BASE_FILTER,
            Column('premarket_change').above_pct('ATRP', 1),
            Column('market_cap_basic') > 20e6
        ). \
        order_by('premarket_change', ascending=False)
    
    PRE_SHORT_MOMENTUM = Query(). \
        select('description', 'sector', 'close', 'premarket_volume', 'market_cap_basic', 'premarket_change', 'premarket_close'). \
        where(
            *BASE_FILTER,
            Column('premarket_change').below_pct('ATRP', -1),
            Column('market_cap_basic') > 20e6
        ). \
        order_by('premarket_change', ascending=True)
    
    POST_LONG_MOMENTUM = Query(). \
        select('description', 'sector', 'close', 'postmarket_volume', 'market_cap_basic', 'postmarket_change', 'postmarket_close'). \
        where(
            *BASE_FILTER,
            Column('postmarket_change').above_pct('ATRP', 1),
            Column('market_cap_basic') > 20e6
        ). \
        order_by('postmarket_change', ascending=False)
    
    POST_SHORT_MOMENTUM = Query(). \
        select('description', 'sector', 'close', 'postmarket_volume', 'market_cap_basic', 'postmarket_change', 'postmarket_close'). \
        where(
            *BASE_FILTER,
            Column('postmarket_change').below_pct('ATRP', -1),
            Column('market_cap_basic') > 20e6
        ). \
        order_by('postmarket_change', ascending=True)
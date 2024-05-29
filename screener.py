from tradingview_screener import Query, Column

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
        order_by('change|5', ascending=True)
}


class Screener:
    
    def scan(self):
        while True:
            match get_current_session():
                case 'MAIN':
                    self._scan_main()
                
    def _scan_main(self):
        pass

    
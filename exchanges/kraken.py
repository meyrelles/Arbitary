from decimal import Decimal

from exchanges.base import Exchange
from exchanges.helpers import get_response


class Kraken(Exchange):

    TICKER_URL = 'https://api.kraken.com/0/public/Trades?pair=%s'
    DEPTH_URL = 'https://api.kraken.com/0/public/Depth?pair=%s'
    PAIR = ''

    @classmethod
    def init2(self, turl):
        self.PAIR = turl 

    @classmethod
    def get_current_price(cls, pair=''):
        data = get_response(cls.TICKER_URL %  cls.PAIR)
        price = data['result'][cls.PAIR][-1][0]
        return Decimal(str(price))

    @classmethod
    def get_current_bid(cls, pair=''):
        data = get_response(cls.DEPTH_URL % cls.PAIR)
        price = data['result'][cls.PAIR]['bids'][0][0]
        return Decimal(str(price))

    @classmethod
    def get_current_ask(cls, pair=''):
        data = get_response(cls.DEPTH_URL % cls.PAIR)
        price = data['result'][cls.PAIR]['asks'][0][0]
        return Decimal(str(price))

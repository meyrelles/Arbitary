from exchanges.base import Exchange


class Poloniex(Exchange):

    TICKER_URL = 'https://poloniex.com/public?command=returnTicker'
    PAIR = ''
    
    @classmethod
    def init2(self, turl):
        self.PAIR = turl

    @classmethod
    def _current_price_extractor(cls, data):
        return data.get(cls.PAIR).get('last')

    @classmethod
    def _current_bid_extractor(cls, data):
        return data.get(cls.PAIR).get('highestBid')

    @classmethod
    def _current_ask_extractor(cls, data):
        return data.get(cls.PAIR).get('lowestAsk')
